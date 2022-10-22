import logging
import time
import yaml
import win32gui
import pyautogui
from pyscreeze import Box, Point
from log import Log

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
config = {}
log = None


def load_config():
    with open('./config.yaml', encoding="utf-8") as f:
        global config, log
        config = yaml.safe_load(f.read())
        config['vote']['checkbox'].sort()
        log = Log(name='vote', log_level=logging._nameToLevel[config['log']['level']])


def center(box):
    return Point(box[0] + int(box[2] / 2), box[1] + int(box[3] / 2))


def locateAllCenterOnScreen(image, **kwargs):
    return [center(box) for box in pyautogui.locateAllOnScreen(image, **kwargs)]


def getX(percent):
    return int(SCREEN_WIDTH * percent)


def getY(percent):
    return int(SCREEN_HEIGHT * percent)


def getWindowInfo(className, title):
    """
    获取投票窗口的信息
    """
    handle = win32gui.FindWindow(className, title)
    if handle == 0:
        log.warning('未找到投票窗口')
        return -1, -1, -1, -1
    return win32gui.GetWindowRect(handle)


def getAttendLabelPosition(region):
    """
    获取“未参与”图标左上角的坐标
    """
    return pyautogui.locateOnScreen('./pic/未参与.png', region=region)


def getButtonCenterPostion(region):
    """
    获取投票类型（单选或多选）和一个包含所有选项按钮中心坐标的列表
    """
    position = getRadioCenterPosition(region)
    if len(position) > 0:
        return (0, position)  # 单选
    else:
        return (1, getCheckBoxCenterPosition(region))  # 多选


def getRadioCenterPosition(region):
    """
    获取单选按钮中心的坐标
    """
    return locateAllCenterOnScreen('./pic/radio.png', region=region)


def getCheckBoxCenterPosition(region):
    """
    获取多选按钮中心的坐标
    """
    return locateAllCenterOnScreen('./pic/checkbox.png', region=region)


def getVoteEndLabelPosition(region):
    """
    获取“已结束”图标左上角的坐标
    """
    return pyautogui.locateCenterOnScreen('./pic/已结束.png', region=region)


def isVoteEnd(region):
    return getVoteEndLabelPosition(region) is not None


def getBackToListCenterPosition(region):
    """
    获取“返回列表”按钮中心的坐标
    """
    return pyautogui.locateCenterOnScreen('./pic/返回列表.png', region=region)


def getSubmitCenterPosition(region):
    """
    获取“提交”按钮中心的坐标
    """
    return pyautogui.locateCenterOnScreen('./pic/提交.png', region=region)


def vote(position: Box, left_region, bottom_region, scroll_point):
    """
    投票
    """
    label_left, label_top = position.left, position.top
    pyautogui.click(label_left + getX(0.0078125), label_top - getY(0.01388889))  # 进入投票详情页
    time.sleep(config['vote']['wait'])
    pyautogui.moveTo(scroll_point)
    time.sleep(0.5)
    pyautogui.vscroll(-left_region[3])  # 如果选项特别多，需要下滑鼠标滚轮才能显示完全
    vote_type, button_position = getButtonCenterPostion(left_region)
    list_len = len(button_position)
    if list_len > 0:
        if vote_type == 0:  # 单选
            choice = config['vote']['radio']
            if (choice > list_len):
                choice = list_len
            pyautogui.click(button_position[choice - 1])
        else:  # 多选
            for c in config['vote']['checkbox']:
                if c > list_len:
                    pyautogui.click(button_position[list_len - 1])
                    break
                time.sleep(0.5)
                pyautogui.click(button_position[c - 1])

    else:
        log.warning('未找到选项按钮位置，返回列表')
        pyautogui.click(getBackToListCenterPosition(bottom_region))  # 点击返回列表
        return
    time.sleep(0.5)
    pyautogui.click(getSubmitCenterPosition(bottom_region))  # 点击提交
    time.sleep(config['vote']['wait'])
    pyautogui.click(getBackToListCenterPosition(bottom_region))  # 点击返回列表


def main():
    load_config()
    log.debug(f'分辨率：{SCREEN_WIDTH}×{SCREEN_HEIGHT}')
    log.debug(f'配置：{config}')
    log.info('请打开腾讯会议的投票窗口，5秒后开始自动投票')
    time.sleep(5)
    while True:
        left, top, right, bottom = getWindowInfo(config['window']['class'], config['window']['title'])
        if left > -1:
            width = right - left  # 窗口宽度
            height = bottom - top  # 窗口高度
            left_region = (left, top, int(width * 0.2), bottom - top)  # 窗口左侧 1/4 区域
            position = getAttendLabelPosition(left_region)
            if position is not None and not isVoteEnd((position.left + getX(0.1359375), position.top - getY(0.025), getX(0.02421875), getY(0.01805556))):
                bottom_region = (left, int(top + height * 0.8), width, int(height * 0.2))  # 窗口底部 1/4 区域
                scroll_point = (position.left, int(top + 0.5 * height))  # 鼠标滚轮下滑位置
                vote(position, left_region, bottom_region, scroll_point)
            else:
                log.debug('暂无未投票的投票')
        time.sleep(config['vote']['interval'])


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exit')
