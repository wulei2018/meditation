# 5 Minute Meditation（五分钟冥想）

一个简单而强大的冥想网站，帮助用户通过短时间的冥想获得深度放松。

## 功能特点

- 多种冥想时长选择（3-20分钟）
- 多种冥想风格
- 高质量引导视频
- 响应式设计，支持各种设备
- 简单直观的用户界面

## 技术栈

- HTML5
- CSS3 (Tailwind CSS)
- JavaScript (Vue.js 3)
- Video.js 用于视频播放

## 项目结构

```
/
├── index.html          # 主页面
├── assets/            # 静态资源
│   ├── css/          # 样式文件
│   ├── js/           # JavaScript文件
│   ├── videos/       # 视频文件
│   └── images/       # 图片资源
└── README.md         # 项目说明
```

## 开始使用

1. 克隆项目到本地：
```bash
git clone [repository-url]
```

2. 打开项目目录：
```bash
cd 5minutemeditation
```

3. 在浏览器中打开 `index.html` 文件，或使用本地服务器运行项目：
```bash
# 使用 Python 启动简单的 HTTP 服务器
python -m http.server 8000
```

4. 访问 `http://localhost:8000` 即可使用

## 使用说明

1. 选择冥想时长（3、5、10、15或20分钟）
2. 选择冥想风格（正念冥想、呼吸冥想等）
3. 点击播放开始冥想
4. 使用"换一批"按钮可以切换不同的冥想视频

## 注意事项

- 请确保有稳定的网络连接以流畅播放视频
- 建议使用耳机以获得更好的体验
- 选择安静的环境进行冥想

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 许可证

MIT License 