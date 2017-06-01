# encoding=utf-8
# ----------------------------------------
# 语言：Python2.7
# 日期：2017-05-01
# 作者：九茶<http://blog.csdn.net/bone_ace>
# 功能：破解四宫格图形验证码，登录m.weibo.cn
# ----------------------------------------
import numpy
import time
import random
from PIL import Image
from math import sqrt
from scrapyPro1.scrapyPro1.ims import ims
from io import StringIO,BytesIO
from selenium import webdriver
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
PIXELS = []
from scrapyPro1.scrapyPro1.test import check_sameImg

def getExactly(im):
    """ 精确剪切"""
    imin = -1
    imax = -1
    jmin = -1
    jmax = -1
    row = im.size[0]
    col = im.size[1]
    for i in range(row):
        for j in range(col):
            if im.load()[i, j] != 255:
                imax = i
                break
        if imax == -1:
            imin = i

    for j in range(col):
        for i in range(row):
            if im.load()[i, j] != 255:
                jmax = j
                break
        if jmax == -1:
            jmin = j
    return (imin + 1, jmin + 1, imax + 1, jmax + 1)


def getType(browser):
    """ 识别图形路径 """
    ttype = ''
    time.sleep(5.5)
    im0 = Image.open(BytesIO(browser.get_screenshot_as_png()))
    box = browser.find_element_by_id('patternCaptchaHolder')
    # box = browser.find_element_by_class_name("patt-holder-body")
    print(box.location)
    print(box.size)

    im = im0.crop((int(box.location['x'])+90 , int(box.location['y'])+190, int(box.location['x']) + box.size['width'] +90, int(box.location['y']) + box.size['height'] +130 )).convert('L')
    im.save('im.jpg')
    newBox = getExactly(im)
    im = im.crop(newBox)
    im.save('im1.jpg')
    width = im.size[0]
    height = im.size[1]
    for png in ims.keys():

        isGoingOn = True
        for i in range(width):
            for j in range(height):
                if ((im.load()[i, j] >= 245 and ims[png][i][j] < 245) or (im.load()[i, j] < 245 and ims[png][i][j] >= 245)) and abs(ims[png][i][j] - im.load()[i, j]) > 10: # 以245为临界值，大约245为空白，小于245为线条；两个像素之间的差大约10，是为了去除245边界上的误差
                    isGoingOn = False
                    break
            if isGoingOn is False:
                ttype = ''
                break
            else:
                ttype = png
        else:
            break
    px0_x = box.location['x'] + 40 + newBox[0]
    px1_y = box.location['y'] + 130 + newBox[1]
    PIXELS.append((px0_x, px1_y))
    PIXELS.append((px0_x + 100, px1_y))
    PIXELS.append((px0_x, px1_y + 100))
    PIXELS.append((px0_x + 100, px1_y + 100))
    return ttype


def move(browser, coordinate, coordinate0):
    """ 从坐标coordinate0，移动到坐标coordinate """
    time.sleep(0.05)
    length = sqrt((coordinate[0] - coordinate0[0]) ** 2 + (coordinate[1] - coordinate0[1]) ** 2)  # 两点直线距离
    if length < 4:  # 如果两点之间距离小于4px，直接划过去
        ActionChains(browser).move_by_offset(coordinate[0] - coordinate0[0], coordinate[1] - coordinate0[1]).perform()
        return
    else:  # 递归，不断向着终点滑动
        step = random.randint(3, 5)
        x = int(step * (coordinate[0] - coordinate0[0]) / length)  # 按比例
        y = int(step * (coordinate[1] - coordinate0[1]) / length)
        ActionChains(browser).move_by_offset(x, y).perform()
        move(browser, coordinate, (coordinate0[0] + x, coordinate0[1] + y))


def draw(browser, ttype):
    """ 滑动 """
    if len(ttype) == 4:
        px0 = PIXELS[int(ttype[0]) - 1]
        login = browser.find_element_by_id('loginAction')
        ActionChains(browser).move_to_element(login).move_by_offset(px0[0] - login.location['x'] - int(login.size['width'] / 2), px0[1] - login.location['y'] - int(login.size['height'] / 2)).perform()
        browser.execute(Command.MOUSE_DOWN, {})

        px1 = PIXELS[int(ttype[1]) - 1]
        move(browser, (px1[0], px1[1]), px0)

        px2 = PIXELS[int(ttype[2]) - 1]
        move(browser, (px2[0], px2[1]), px1)

        px3 = PIXELS[int(ttype[3]) - 1]
        move(browser, (px3[0], px3[1]), px2)
        browser.execute(Command.MOUSE_UP, {})
    else:
        print ('Sorry! Failed! Maybe you need to update the code.')
def check_is_sameImg(image):
    pass

if __name__ == '__main__':
    # dcap = dict(DesiredCapabilities.PHANTOMJS)  # PhantomJS需要使用老版手机的user-agent，不然验证码会无法通过
    # dcap["phantomjs.page.settings.userAgent"] = (
    #     "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
    # )
    # browser = webdriver.PhantomJS(desired_capabilities=dcap)
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    options.add_argument(
        'user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
    # options.add_argument('--user-data-dir=C:/Users/0/AppData/Local/Google/Chrome/User Data')
    browser = webdriver.Chrome(chrome_options=options)
    # browser = webdriver.Chrome()
    # browser = webdriver.Firefox()
    browser.set_window_size(height=1050, width=840)
    # browser.get('http://mail.haidilao.com')
    browser.get('https://passport.weibo.cn/signin/login?entry=mweibo&r=http://weibo.cn/')

    time.sleep(5)
    name = browser.find_element_by_id('loginName')
    psw = browser.find_element_by_id('loginPassword')
    login = browser.find_element_by_id('loginAction')
    name.send_keys('13537415579')  # 测试账号
    psw.send_keys('passw0rd')
    login.click()

    ttype = getType(browser)  # 识别图形路径
    print ('Result: %s!' % ttype)
    draw(browser, ttype)  # 滑动破解
    check_sameImg()
    time.sleep(10)
    browser.close()

