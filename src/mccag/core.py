from io import BytesIO
from PIL import Image, ImageFilter


class AvatarRenderer:
    player_texture: Image.Image

    def __init__(self, player_texture: BytesIO) -> None:
        """
        创建 `AvatarGenerator` 对象

        Example:

        ```python
        image = AvatarGenerator(skin_texture).generate()
        ```

        ---

        Args:
            player_texture (BytesIO): 玩家皮肤材质文件，支持 `64x64` 和 `128x128`
        """
        self.player_texture = Image.open(player_texture)

    def _create_canvas(self) -> Image.Image:
        # 创建画布并缩放至 128x128
        canvas_size = (1000, 1000)
        canvas = Image.new("RGBA", canvas_size, (255, 255, 255, 0))
        resized_player_texture = self.player_texture.resize((128, 128), Image.Resampling.NEAREST)

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
            ((16, 16, 32, 32), 26.875, (287, 131)),
            ((80, 16, 96, 32), 30.8125, (254, 107)),
        ]

        for operation in operations:
            crop_box, scale_factor, paste_position = operation

            cropped_image = resized_player_texture.crop(crop_box)
            new_size = (
                int(cropped_image.size[0] * scale_factor),
                int(cropped_image.size[1] * scale_factor),
            )
            bordered_size = (new_size[0] + 30, new_size[1] + 30)
            bordered_image = Image.new("RGBA", bordered_size, (0, 0, 0, 0))
            bordered_image.paste(cropped_image.resize(new_size, Image.Resampling.NEAREST), (15, 15))

            mask = bordered_image.split()[3]
            solid_image = Image.new("RGBA", bordered_image.size, (75, 85, 142, 255))
            shadow_image = Image.composite(solid_image, Image.new("RGBA", bordered_image.size), mask)
            blurred_shadow = shadow_image.filter(ImageFilter.GaussianBlur(7))
            alpha = blurred_shadow.split()[3].point(lambda p: p * 0.5)
            blurred_shadow.putalpha(alpha)

            shadow_position = (paste_position[0] - 15, paste_position[1] - 10)
            canvas.paste(blurred_shadow, shadow_position, blurred_shadow)

            adjusted_paste_position = (paste_position[0] - 15, paste_position[1] - 15)
            canvas.paste(bordered_image, adjusted_paste_position, bordered_image)

        return canvas

    def render(self) -> BytesIO:
        """
        生成图片
        """
        canvas = self._create_canvas()

        output_image = BytesIO()
        canvas.save(output_image, "PNG")

        return output_image
