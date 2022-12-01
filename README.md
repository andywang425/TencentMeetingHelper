# TencentMeetingHelper

腾讯会议助手，自动签到、投票。

## 环境要求

- Windows
- 显示器的分辨率比例为 16:9 且分别率至少为 1920×1080

## 安装

前往[Release](https://github.com/andywang425/TencentMeetingHelper/releases/latest)，下载压缩包`TencentMeetingHelper.7z`并解压。
打开`config.yaml`，根据需要修改配置。最后双击`TencentMeetingHelper.exe`即可运行。

<details>
<summary>从源代码安装</summary>

1. 环境要求：Python 3.6+

2. Clone 本项目

```
git clone https://github.com/andywang425/TencentMeetingHelper.git
```

3. 安装依赖

```
pip install -r requirements.txt
```

4. 将配置文件样例`config.example.yaml`复制并重命名为`config.yaml`，根据需要修改配置。

```
copy config.example.yaml config.yaml | start config.yaml
```

5. 运行

```
python main.py
```

</details>

## 使用说明

脚本通过 Win32 API、图像识别和键鼠操作来实现各项功能，所以需要让腾讯会议窗口显示在前台，且脚本在进行操作的时候不能乱动鼠标和键盘。

使用前请先进入会议并打开投票窗口，确保投票窗口，“xxx 邀请您使用签到”窗口（默认在右上角）和签到窗口（默认在屏幕中心）不会互相遮挡。

如果启用了自动投票功能，请将缩放（Windows 设置-系统-屏幕-缩放与布局）改为 125% 然后再打开腾讯会议。

如果启用了自动签到功能，请不要手动打开签到窗口，也不要在脚本打开签到窗口后拉伸签到窗口，否则脚本将无法正常运行。

## 功能介绍

### 自动投票

打开腾讯会议的投票窗口并将其放到合适的位置，脚本会根据设置自动参加投票。

**已知问题**

- 目前仅支持只有一个问题的投票。如果遇到有多个问题的投票可能会反复进入、退出该投票，直到有新的投票出现。

### 自动签到

检测到“xxx 邀请您使用签到”窗口后脚本会点击“打开应用”按钮，然后在签到窗口中点击“点击签到”按钮。

**已知问题**

- 有时签到窗口顶部会显示提示信息，这个提示可能会影响脚本运行，不过通常只会在腾讯会议更新后第一次打开签到窗口时显示。

## 更新计划

- 支持多个问题的投票
- 自动投票支持任意缩放倍数

## 许可证

TencentMeetingHelper 基于 [MIT](LICENSE) 协议开源。
