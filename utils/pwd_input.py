import os
import re
import sys
import time

"""
# 密码控件坐标点击方法模块
- 依赖环境：
    adb
    python3
"""

# 手机配置信息，设备序列号deviceName
desire_caps = {
    "deviceName": "000001f6acb7e14e"
}

# 密码键盘相对于屏幕坐标百分比映射，银盛小Y管家密码键盘
key_map = {
    # 数字键盘字符坐标百分比映射
    "number": {
        "1": {
            "x": 0.167,
            "y": 0.796
        },
        "2": {
            "x": 0.5,
            "y": 0.796
        },
        "3": {
            "x": 0.833,
            "y": 0.796
        },
        "4": {
            "x": 0.167,
            "y": 0.854
        },
        "5": {
            "x": 0.5,
            "y": 0.854
        },
        "6": {
            "x": 0.833,
            "y": 0.854
        },
        "7": {
            "x": 0.167,
            "y": 0.912
        },
        "8": {
            "x": 0.5,
            "y": 0.912
        },
        "9": {
            "x": 0.833,
            "y": 0.912
        },
        "num_letter_switcher": {
            "x": 0.13,
            "y": 0.97
        },
        "0": {
            "x": 0.5,
            "y": 0.97
        },
        "num_back": {
            "x": 0.87,
            "y": 0.97
        }
    },
    # 字母键盘字符坐标百分比映射
    "letter": {
        "q": {
            "x": 0.05,
            "y": 0.796
        },
        "w": {
            "x": 0.15,
            "y": 0.796
        },
        "e": {
            "x": 0.25,
            "y": 0.796
        },
        "r": {
            "x": 0.35,
            "y": 0.796
        },
        "t": {
            "x": 0.45,
            "y": 0.796
        },
        "y": {
            "x": 0.55,
            "y": 0.796
        },
        "u": {
            "x": 0.65,
            "y": 0.796
        },
        "i": {
            "x": 0.75,
            "y": 0.796
        },
        "o": {
            "x": 0.85,
            "y": 0.796
        },
        "p": {
            "x": 0.95,
            "y": 0.796
        },
        "a": {
            "x": 0.1,
            "y": 0.854
        },
        "s": {
            "x": 0.2,
            "y": 0.854
        },
        "d": {
            "x": 0.3,
            "y": 0.854
        },
        "f": {
            "x": 0.4,
            "y": 0.854
        },
        "g": {
            "x": 0.5,
            "y": 0.854
        },
        "h": {
            "x": 0.6,
            "y": 0.854
        },
        "j": {
            "x": 0.7,
            "y": 0.854
        },
        "k": {
            "x": 0.8,
            "y": 0.854
        },
        "l": {
            "x": 0.9,
            "y": 0.854
        },
        "z": {
            "x": 0.2,
            "y": 0.912
        },
        "cap_switcher": {
            "x": 0.1,
            "y": 0.912
        },
        "x": {
            "x": 0.3,
            "y": 0.912
        },
        "c": {
            "x": 0.4,
            "y": 0.912
        },
        "v": {
            "x": 0.5,
            "y": 0.912
        },
        "b": {
            "x": 0.6,
            "y": 0.912
        },
        "n": {
            "x": 0.7,
            "y": 0.912
        },
        "m": {
            "x": 0.8,
            "y": 0.912
        },
        "letter_back": {
            "x": 0.9,
            "y": 0.912
        },
        "letter_num_switcher": {
            "x": 0.13,
            "y": 0.97
        },
        "space_key": {
            "x": 0.5,
            "y": 0.97
        },
        "letter_symbol_switcher": {
            "x": 0.9,
            "y": 0.97
        }
    },
    # 符号键盘字符坐标百分比映射
    "symbol": {
        "!": {
            "x": 0.05,
            "y": 0.796
        },
        "@": {
            "x": 0.15,
            "y": 0.796
        },
        "#": {
            "x": 0.25,
            "y": 0.796
        },
        "$": {
            "x": 0.35,
            "y": 0.796
        },
        "%": {
            "x": 0.45,
            "y": 0.796
        },
        "^": {
            "x": 0.55,
            "y": 0.796
        },
        "&": {
            "x": 0.65,
            "y": 0.796
        },
        "*": {
            "x": 0.75,
            "y": 0.796
        },
        "(": {
            "x": 0.85,
            "y": 0.796
        },
        ")": {
            "x": 0.95,
            "y": 0.796
        },
        "'": {
            "x": 0.05,
            "y": 0.854
        },
        "\"": {
            "x": 0.15,
            "y": 0.854
        },
        "=": {
            "x": 0.25,
            "y": 0.854
        },
        "_": {
            "x": 0.35,
            "y": 0.854
        },
        ":": {
            "x": 0.45,
            "y": 0.854
        },
        ";": {
            "x": 0.55,
            "y": 0.854
        },
        "?": {
            "x": 0.65,
            "y": 0.854
        },
        "~": {
            "x": 0.75,
            "y": 0.854
        },
        "|": {
            "x": 0.85,
            "y": 0.854
        },
        ".": {
            "x": 0.95,
            "y": 0.854
        },
        "+": {
            "x": 0.1,
            "y": 0.912
        },
        "-": {
            "x": 0.2,
            "y": 0.912
        },
        "\\": {
            "x": 0.3,
            "y": 0.912
        },
        "/": {
            "x": 0.4,
            "y": 0.912
        },
        "[": {
            "x": 0.5,
            "y": 0.912
        },
        "]": {
            "x": 0.6,
            "y": 0.912
        },
        "{": {
            "x": 0.7,
            "y": 0.912
        },
        "}": {
            "x": 0.8,
            "y": 0.912
        },
        "symbol_back": {
            "x": 0.9,
            "y": 0.912
        },
        "symbol_num_switcher": {
            "x": 0.13,
            "y": 0.97
        },
        ",": {
            "x": 0.9,
            "y": 0.97
        },
        "。": {
            "x": 0.3,
            "y": 0.97
        },
        "<": {
            "x": 0.4,
            "y": 0.97
        },
        ">": {
            "x": 0.5,
            "y": 0.97
        },
        "€": {
            "x": 0.6,
            "y": 0.97
        },
        "£": {
            "x": 0.7,
            "y": 0.97
        },
        "￥": {
            "x": 0.8,
            "y": 0.97
        },
        "symbol_letter_switcher": {
            "x": 0.87,
            "y": 0.97
        }
    }
}


# 获取应用窗口分辨率
def get_window_screen(sn):
    try:
        cm = os.popen(f'adb -s {sn} shell dumpsys window displays | findstr mStableFullscreen')
        con = cm.read()
        cm.close()
    except Exception as e:
        print("adb环境异常")
        raise e
    reg = r'\d+'
    x_pix = int(re.findall(reg, con)[-2])
    y_pix = int(re.findall(reg, con)[-1])
    return x_pix, y_pix


# 密码字符串点击顺序转坐标映射
def pwd_read(pwd_path, user_pwd):
    """
    密码字符串转密码控件坐标输入顺序列表方法：
    :param pwd_path：密码控件字符位置坐标与屏幕相对百分比映射
    :param user_pwd：密码字符串
    :return: case_steps, 密码输入步骤坐标及控件内容列表（例：密码123,对应返回[(0.167,0.796,"1"),(0.5,0.796,"2"),(0.833,0.796,"")]）
    """
    # 密码坐标百分比映射表
    key_read = pwd_path
    kb_status = '00'  # 初始化键盘状态：数字键盘=00(初始状态)；小写字母=01；字符键盘=02
    case_steps = []  # 初始化步骤列表
    for keys in user_pwd:
        # 判断字符为数字
        if keys.isdigit():
            # 数字字符转int
            keys = int(keys)
            # 检查键盘状态
            if kb_status == '00':
                key_data = key_read['number'][f'{keys}']
                steps = [(key_data['x'], key_data['y'], keys)]
                case_steps = case_steps + steps
                kb_status = "00"
            elif kb_status == '01':
                letter_num_switcher = key_read['letter']['letter_num_switcher']
                key_data = key_read['number'][f'{keys}']
                steps = [(letter_num_switcher['x'], letter_num_switcher['y'], 'letter_num_switcher'),
                         (key_data['x'], key_data['y'], keys)]
                case_steps = case_steps + steps
                kb_status = "00"
            elif kb_status == '02':
                symbol_num_switcher = key_read['symbol']['symbol_num_switcher']
                key_data = key_read['number'][f'{keys}']
                steps = [(symbol_num_switcher['x'], symbol_num_switcher['y'], 'symbol_num_switcher'),
                         (key_data['x'], key_data['y'], keys)]
                case_steps = case_steps + steps
                kb_status = "00"
        # 判断字符为小写字母
        elif keys.islower():
            if kb_status == '01':
                key_data = key_read['letter'][f'{keys}']
                steps = [(key_data['x'], key_data['y'], keys)]
                case_steps = case_steps + steps
                kb_status = "01"
            elif kb_status == '00':
                num_letter_switcher = key_read['number']['num_letter_switcher']
                key_data = key_read['letter'][f'{keys}']
                steps = [(num_letter_switcher['x'], num_letter_switcher['y'], 'num_letter_switcher'),
                         (key_data['x'], key_data['y'], keys)]
                case_steps = case_steps + steps
                kb_status = "01"
            elif kb_status == '02':
                symbol_letter_switcher = key_read['symbol']['symbol_letter_switcher']
                key_data = key_read['letter'][f'{keys}']
                steps = [(symbol_letter_switcher['x'], symbol_letter_switcher['y'], 'symbol_letter_switcher'),
                         (key_data['x'], key_data['y'], keys)]
                case_steps = case_steps + steps
                kb_status = "01"
        # 判断字符为大写字母
        elif keys.isupper():
            if kb_status == '01':
                cap_switcher = key_read['letter']['cap_switcher']
                key_data = key_read['letter'][f'{keys.lower()}']
                steps = [(cap_switcher['x'], cap_switcher['y'], 'cap_switcher'),
                         (key_data['x'], key_data['y'], keys)]
                case_steps = case_steps + steps
                kb_status = "01"
            elif kb_status == '00':
                num_letter_switcher = key_read['number']['num_letter_switcher']
                switch_cap = key_read['letter']['cap_switcher']
                key_data = key_read['letter'][f'{keys.lower()}']
                steps = [(num_letter_switcher['x'], num_letter_switcher['y'], 'num_letter_switcher'),
                         (switch_cap['x'], switch_cap['y'], 'cap_switcher'),
                         (key_data['x'], key_data['y'], keys)]
                case_steps = case_steps + steps
                kb_status = "01"
            elif kb_status == '02':
                symbol_letter_switcher = key_read['symbol']['symbol_letter_switcher']
                cap_switcher = key_read['letter']['cap_switcher']
                key_data = key_read['letter'][f'{keys.lower()}']
                steps = [(symbol_letter_switcher['x'], symbol_letter_switcher['y'], 'symbol_letter_switcher'),
                         (cap_switcher['x'], cap_switcher['y'], 'cap_switcher'),
                         (key_data['x'], key_data['y'], keys)]
                case_steps = case_steps + steps
                kb_status = "01"
        # 判断字符为其它字符（非数字/字母）
        else:
            if kb_status == '02':
                key_data = key_read['symbol'][f'{keys}']
                steps = [(key_data['x'], key_data['y'], keys)]
                case_steps = case_steps + steps
                kb_status = "02"
            elif kb_status == '00':
                num_letter_switcher = key_read['number']['num_letter_switcher']
                letter_symbol_switcher = key_read['letter']['letter_symbol_switcher']
                key_data = key_read['symbol'][f'{keys}']
                steps = [(num_letter_switcher['x'], num_letter_switcher['y'], 'num_letter_switcher'),
                         (letter_symbol_switcher['x'], letter_symbol_switcher['y'], 'letter_symbol_switcher'),
                         (key_data['x'], key_data['y'], keys)]
                case_steps = case_steps + steps
                kb_status = "02"
            elif kb_status == '01':
                letter_symbol_switcher = key_read['letter']['letter_symbol_switcher']
                key_data = key_read['symbol'][f'{keys}']
                steps = [(letter_symbol_switcher['x'], letter_symbol_switcher['y'], 'letter_symbol_switcher'),
                         (key_data['x'], key_data['y'], keys)]
                case_steps = case_steps + steps
                kb_status = "02"
    return case_steps


# 密码控件坐标点击输入
def pwd_input(user_pwd):
    # 使用adb命令获取手机物理分辨率
    sn = desire_caps["deviceName"]
    scr = get_window_screen(sn)
    x_pix = scr[0]
    y_pix = scr[1]
    # 调用密码字符串转密码控件坐标输入顺序列表方法
    password = pwd_read(key_map, user_pwd)
    # 遍历点击密码输入顺序列表
    for steps in password:
        x_tap = int(steps[0] * x_pix)
        y_tap = int(steps[1] * (y_pix))
        ele_tap = steps[2]
        tap_cmd = f"adb -s {sn} shell input tap {x_tap} {y_tap}"
        print(f"点击坐标:({x_tap},{y_tap})，键盘字符控件:[{ele_tap}]")
        os.popen(tap_cmd)
        time.sleep(0.3)


if __name__ == "__main__":
    pwd = str(sys.argv[1])
    pwd_input(pwd)
    # print("测试调试：", pwd_input(str(pwd)))
    # pwd = "test123456"
    # print(get_screen("test"))
