from io import BytesIO
from typing import Annotated, Literal

from fastapi import Query
from PIL import Image, ImageFilter, ImageOps

type AvatarTypes = Annotated[
    Literal["full", "head"], Query(description="Type of avatar to generate", example="full")
]


class AvatarRenderer:
    player_texture: Image.Image
    avatar_type: Literal["full", "head"] = "full"

    def __init__(self, player_texture: BytesIO) -> None:
        """
        创建 `AvatarGenerator` 对象

        Example:

        ```python
        image = AvatarGenerator(skin_texture, avatar_type='head').render()
        ```

        ---

        Args:
            player_texture (BytesIO): 玩家皮肤材质文件，支持 `64x64` 和 `128x128`
            avatar_type (str): 头像类型，支持 'full' 和 'head'
        """
        self.player_texture = Image.open(player_texture)

    def _create_canvas(self) -> Image.Image:
        # 创建画布并缩放至 128x128
        canvas_size = (1000, 1000) if self.avatar_type == "full" else (500, 500)
        canvas = Image.new("RGBA", canvas_size, (255, 255, 255, 0))

        skin_size = self.player_texture.size

        if skin_size == (64, 32):
            resized_texture_image = self.player_texture.resize((128, 64), Image.Resampling.NEAREST)
        else:
            resized_texture_image = self.player_texture.resize((128, 128), Image.Resampling.NEAREST)

        if self.avatar_type == "head":  # 生成头部的
            if skin_size == (64, 32):
                operations = [
                    ((16, 16, 32, 32), 18.375, (100, 105)),
                    ((80, 16, 96, 32), 19.375, (92, 97)),
                ]
            else:
                operations = [
                    ((16, 16, 32, 32), 18.375, (100, 105)),
                    ((80, 16, 96, 32), 19.375, (92, 97)),
                ]
        else:  # 生成全身 默认
            if skin_size == (64, 32):
                # 1.7 format
                operations = [
                    ((8, 40, 16, 64), 8.375, (434, 751)),  # RL
                    ((8, 40, 16, 64), 8.375, (505, 751), True),  # LL, use RL mirror
                    ((86, 40, 92, 64), 8.167, (388, 561)),  # RA
                    ((86, 40, 92, 64), 8.167, (566, 561), True),  # LA, use RA mirror
                    ((40, 40, 56, 64), 8.0625, (437, 561)),  # BF
                    ((16, 16, 32, 32), 26.875, (287, 131)),  # HF
                    ((80, 16, 96, 32), 30.8125, (254, 107)),  # HF L2
                ]
            else:
                # 1.8 format
                operations = [
                    ((8, 40, 16, 64), 8.375, (434, 751)),
                    ((8, 72, 16, 96), 9.375, (428, 737)),
                    ((40, 104, 48, 128), 8.375, (505, 751)),
                    ((8, 104, 16, 128), 9.375, (503, 737)),
                    ((86, 40, 92, 64), 8.167, (388, 561)),
                    ((88, 72, 94, 96), 9.5, (382, 538)),
                    ((74, 104, 80, 128), 8.167, (566, 561)),
                    ((104, 104, 110, 128), 9.5, (564, 538)),
                    ((40, 40, 56, 64), 8.0625, (437, 561)),
                    ((40, 72, 56, 96), 8.6575, (432, 555)),
                    ((16, 16, 32, 32), 26.875, (287, 131)),  # HF
                    ((80, 16, 96, 32), 30.8125, (254, 107)),  # HF L2
                ]

        for operation in operations:
            crop_box, scale_factor, paste_position, *mirror = operation

            cropped_image = resized_texture_image.crop(crop_box)
            if mirror:
                cropped_image = ImageOps.mirror(cropped_image)

            new_size = (
                int(cropped_image.size[0] * scale_factor),
                int(cropped_image.size[1] * scale_factor),
            )
            bordered_size = (new_size[0] + 30, new_size[1] + 30)
            bordered_image = Image.new("RGBA", bordered_size, (0, 0, 0, 0))
            bordered_image.paste(cropped_image.resize(new_size, Image.Resampling.NEAREST), (15, 15))

            # 创建阴影
            mask = bordered_image.split()[3]  # 仅获取透明度通道
            solid_image = Image.new("RGBA", bordered_image.size, (75, 85, 142, 255))  # 固定颜色，透明背景
            shadow_image = Image.new("RGBA", bordered_image.size, (0, 0, 0, 0))  # 完全透明的背景
            shadow_image.paste(solid_image, (0, 0), mask)  # 使用mask创建阴影
            blurred_shadow = shadow_image.filter(ImageFilter.GaussianBlur(7))
            alpha = blurred_shadow.split()[3].point(lambda p: p * 0.6)
            blurred_shadow.putalpha(alpha)

            shadow_position = (paste_position[0] - 15, paste_position[1] - 10)

            # 创建新的全透明图像并合成阴影
            base_image = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
            base_image.paste(blurred_shadow, shadow_position, blurred_shadow)
            canvas = Image.alpha_composite(canvas, base_image)

            # 粘贴实际图像
            adjusted_paste_position = (paste_position[0] - 15, paste_position[1] - 15)
            canvas.paste(bordered_image, adjusted_paste_position, bordered_image)

        return canvas

    def render(self, avatar_type: Literal["full", "head"] = "full") -> BytesIO:
        """
        生成图片
        """

        self.avatar_type = avatar_type

        canvas = self._create_canvas()

        output_image = BytesIO()
        canvas.save(output_image, "PNG")

        return output_image
