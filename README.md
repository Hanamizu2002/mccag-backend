<div align="center">

# 🥰 MCCAG API

<img src="./assets/logo.png" alt="MCCAG Logo">

_Minecraft Cute Avatar Generator_  
_MC可爱头像生成器_

</div>

> [!NOTE]
> 此项目并非本人原创，思路来自 [Natsusomekeishi/MCCAG](https://github.com/Natsusomekeishi/MCCAG)

## Features 特性

- [x] 从 Minecraft.net 通过 _玩家名_ & _UUID_ 获取源皮肤材质
- [x] 从 [LittleSkin.cn](https://littleskin.cn/) 通过 _玩家名_ & _UUID_ 获取源皮肤材质
- [x] 用户上传皮肤材质文件

## Development 开发

```bash
# install project
pdm install

# sync dependencies
pdm sync --clean

# run dev server
pdm dev
```

## Docker 部署

```bash
# build
docker build -t mccag:latest .

# run
docker run -d -p 80:8023 --name mccag mccag:latest
```
