# TencentMeetingHelper

腾讯会议助手，自动参与投票，自动签到。

## 环境要求

- Windows
- Python 3.6+
- 显示器的分辨率比例为 16:9 且分别率至少为 1920×1080

## 安装

1. Clone 本项目

```
git clone https://github.com/andywang425/TencentMeetingHelper.git
```

2. 安装依赖

```
pip install -r requirements.txt
```

3. 打开配置文件`config.yaml`，根据需要修改配置。

4. 运行

```
python main.py
```

## 使用说明

脚本通过 Win32 API、图像识别和键鼠操作来实现各项功能，所以需要让腾讯会议窗口显示在前台，且脚本在进行操作的时候不能乱动鼠标和键盘。

使用前请先进入会议并打开投票窗口，确保投票窗口，“xxx 邀请您使用签到”窗口（默认在右上角）和签到窗口（默认在中心）不会互相遮挡。

## 功能介绍

### 自动投票

打开腾讯会议的投票窗口并将其放到合适的位置，脚本会根据设置自动参加投票。

**已知问题**

- 在显示器分辨率较低的情况下可能无法正常运行。
- 目前仅支持只有一个问题的投票。如果遇到有多个问题的投票可能会反复进入、退出该投票，直到有新的投票出现。

### 自动签到

检测到“xxx 邀请您使用签到”窗口后脚本会点击“打开应用”按钮，然后在签到窗口中点击“点击签到”按钮。

**已知问题**

- 在显示器分辨率较低的情况下可能无法正常运行。
- 有时签到窗口上方会显示提示，这个提示会影响脚本运行。

## 更新计划

- 支持多个问题的投票
- 优化自动签到
- 优化图像识别在低分辨率机器上的表现。

## 许可证

TencentMeetingHelper 基于 [MIT](LICENSE) 协议开源。
