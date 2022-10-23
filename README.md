# TencentMeetingHelper

腾讯会议助手，可以自动参与投票。其它功能还在开发中。

## 环境要求

- Windows
- Python 3.6+
- 显示器的分辨率不能过低，建议大于 1920×1080

## 安装

Clone 本项目到本地

```
git clone https://github.com/andywang425/TencentMeetingHelper.git
```

安装依赖

```
pip install -r requirements.txt
```

打开配置文件`config.yaml`，根据需要修改配置。

运行

```
python main.py
```

## 说明

脚本通过 Win32 API、图像识别和键鼠操作来实现各项功能，所以不能把腾讯会议窗口最小化，且脚本在进行操作的时候不能乱动鼠标和键盘。

## 功能细节

### 自动投票

打开腾讯会议的投票窗口，脚本会根据设置自动参加投票。目前仅支持只有一个问题的投票。如果遇到有多个问题的投票可能会反复进入、退出该投票，直到有新的投票出现。以后会尝试解决这个问题。

## 更新计划

- 支持多个问题的投票
- 自动签到

## 许可证

TencentMeetingHelper 基于 [MIT](LICENSE) 协议开源。
