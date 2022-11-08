import logging
import math
import threading
import time
import yaml
import win32gui
import pyautogui
from pyscreeze import Box, Point
from log import Log

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
config = {}
log = Log(name='temp')


def load_config():
    try:
        with open('./config.yaml', encoding="utf-8") as f:
            global config, log
            config = yaml.safe_load(f.read())
            config['vote']['checkbox'].sort()
            log = Log(name='vote', log_level=logging._nameToLevel[config['log']['level']])
    except IOError:
        log.critical("无法打开配置文件config.yaml")
        exit(-1)


def center(box):
    return Point(box[0] + int(box[2] / 2), box[1] + int(box[3] / 2))


def locateAllCenterOnScreen(image, **kwargs):
    return [center(box) for box in pyautogui.locateAllOnScreen(image, **kwargs)]


def getX(percent, width=SCREEN_WIDTH, base=0):
    return int(width * percent + base)


def getY(percent, height=SCREEN_HEIGHT, base=0):
    return int(height * percent + base)


def getInviteSignInWindowRect(className) -> tuple[int, int, int, int]:
    """
    获取“邀请您使用签到”弹窗的位置
    """
    list = []

    def callback(hwnd, _param):
        if win32gui.GetClassName(hwnd) == className and win32gui.GetWindowTextLength(hwnd) == 0 and win32gui.IsWindowVisible(hwnd):
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            width = right - left
            height = bottom - top
            if 0 < left < SCREEN_WIDTH and 0 < top < SCREEN_HEIGHT and math.isclose(width / height, 2.5530303, abs_tol=0.1):
                list.append((left, top, right, bottom))

    win32gui.EnumWindows(callback, 0)
    list_len = len(list)
    if list_len == 1:
        return list[0]
    elif (list_len == 0):
        log.debug('暂无“邀请您使用签到”弹窗')
        return -1, -1, -1, -1
    else:
        log.error(f'找到{list_len}个疑似符合要求的“邀请您使用签到”弹窗，请向开发者反馈！')
        return -1, -1, -1, -1


def getSignInWindowRect(className) -> tuple[int, int, int, int]:
    """
    获取签到窗口的位置
    """
    list = []

    def callback(hwnd, _param):
        if win32gui.GetClassName(hwnd) == className and win32gui.GetWindowTextLength(hwnd) == 0 and win32gui.IsWindowVisible(hwnd):
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            width = right - left
            height = bottom - top
            if 0 < left < SCREEN_WIDTH and 0 < top < SCREEN_HEIGHT and math.isclose(width / height, 1.2454545, abs_tol=0.1):
                list.append((left, top, right, bottom))

    win32gui.EnumWindows(callback, 0)
    list_len = len(list)
    if list_len == 1:
        return list[0]
    elif (list_len == 0):
        log.error('未找到签到窗口！')
        return -1, -1, -1, -1
    else:
        log.error(f'找到{list_len}个疑似符合要求的签到窗口，请向开发者反馈！')
        return -1, -1, -1, -1


def getVoteWindowRect(className, title):
    """
    获取投票窗口的位置
    """
    handle = win32gui.FindWindow(className, title)
    if handle == 0:
        log.warning('未找到投票窗口')
        return -1, -1, -1, -1
    return win32gui.GetWindowRect(handle)


def clickOpenAppButton(region):
    """
    点击“打开应用”按钮
    """
    pyautogui.click(getX(0.7655786, region[2], region[0]), getY(0.7272727, region[3], region[1]))


def clickSigninButton(region):
    """
    点击“点击签到”按钮
    """
    return pyautogui.click(getX(0.497810219, region[2], region[0]), getY(0.7, region[3], region[1]))


def getAttendLabelPosition(region):
    """
    获取“未参与”图标左上角的坐标
    """
    return pyautogui.locateOnScreen('./pic/noAttend.png', region=region, confidence=0.8, grayscale=True)


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
    return locateAllCenterOnScreen('./pic/radio.png', region=region, confidence=0.9, grayscale=True)


def getCheckBoxCenterPosition(region):
    """
    获取多选按钮中心的坐标
    """
    return locateAllCenterOnScreen('./pic/checkbox.png', region=region, confidence=0.9, grayscale=True)


def getVoteEndLabelPosition(region):
    """
    获取“已结束”图标左上角的坐标
    """
    return pyautogui.locateOnScreen('./pic/isEnd.png', region=region, confidence=0.8, grayscale=True)


def isVoteEnd(region):
    return getVoteEndLabelPosition(region) is not None


def getBackToListCenterPosition(region):
    """
    获取“返回列表”按钮中心的坐标
    """
    return pyautogui.locateCenterOnScreen('./pic/back2list.png', region=region, grayscale=True)


def getSubmitCenterPosition(region):
    """
    获取“提交”按钮中心的坐标
    """
    return pyautogui.locateCenterOnScreen('./pic/submit.png', region=region, grayscale=True)


def vote(position: Box, left_region, bottom_region, scroll_point):
    """
    投票
    """
    label_left, label_top = position.left, position.top
    pyautogui.click(getX(0.0078125, base=label_left),  getY(-0.01388889, base=label_top))  # 进入投票详情页
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


def task_vote():
    while True:
        left, top, right, bottom = getVoteWindowRect('TXGuiFoundation', '投票')
        if left > -1:
            width = right - left  # 窗口宽度
            height = bottom - top  # 窗口高度
            left_region = (left, top, int(width * 0.2), height)  # 窗口左侧 1/4 区域
            position = getAttendLabelPosition(left_region)
            if position is not None and not isVoteEnd((getX(0.6, width, left), getY(-0.078740157, height, position.top), int(width * 0.4), getY(0.078740157480315, height))):
                log.debug('发现可参加的投票')
                bottom_region = (left, int(top + height * 0.8), width, int(height * 0.2))  # 窗口底部 1/4 区域
                scroll_point = (position.left, int(top + 0.5 * height))  # 鼠标滚轮下滑位置
                vote(position, left_region, bottom_region, scroll_point)
            else:
                log.debug('暂无未投票的投票')
        time.sleep(config['vote']['interval'])


def task_signin():
    while True:
        left, top, right, bottom = getInviteSignInWindowRect('TXGuiFoundation')
        if left > -1:
            log.debug('发现“xxx邀请您使用签到”')
            region = (left, top, right - left, bottom - top)
            time.sleep(0.5)  # 防止弹窗仍在弹出的过程中
            clickOpenAppButton(region)
            time.sleep(config['signin']['interval'])
            left, top, right, bottom = getSignInWindowRect('TXGuiFoundation')
            region = (left, top, right - left, bottom - top)
            clickSigninButton(region)
        time.sleep(config['signin']['interval'])


def wait_for_quit():
    while True:
        input()


def main():
    load_config()
    log.debug(f'分辨率：{SCREEN_WIDTH}×{SCREEN_HEIGHT}')
    log.debug(f'配置：{config}')
    log.info('5秒后开始运行')
    time.sleep(5)
    if config['vote']['enable']:
        threading.Thread(name='vote', target=task_vote, daemon=True).start()
    if config['signin']['enable']:
        threading.Thread(name='signin', target=task_signin, daemon=True).start()
    wait_for_quit()


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print('Exit')
