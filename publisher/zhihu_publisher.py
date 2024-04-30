import sys

import pyperclip
from selenium.webdriver import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

from utils.file_utils import read_file_with_footer, convert_md_to_html, read_file
from utils.selenium_utils import get_html_web_content
from utils.yaml_file_utils import read_jianshu, read_common, read_segmentfault, read_oschina, read_zhihu
import time


def zhihu_publisher(driver):
    zhihu_config = read_zhihu()
    common_config = read_common()

    # 打开新标签页并切换到新标签页
    driver.switch_to.new_window('tab')

    # 浏览器实例现在可以被重用，进行你的自动化操作
    driver.get(zhihu_config['site'])
    time.sleep(2)  # 等待2秒

    # 文章标题
    title = driver.find_element(By.XPATH, '//textarea[contains(@placeholder, "请输入标题")]')
    title.clear()
    title.send_keys(common_config['title'])
    time.sleep(2)  # 等待3秒

    # 文章内容 html版本
    content_file = common_config['content']
    # 注意，zhihu 不能识别转换过后的代码块格式
    content_file_html = convert_md_to_html(content_file)
    get_html_web_content(driver, content_file_html)
    time.sleep(2)  # 等待2秒
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(1)  # 等待1秒
    # 用的是CodeMirror,不能用元素赋值的方法，所以我们使用拷贝的方法
    cmd_ctrl = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL
    action_chains = webdriver.ActionChains(driver)
    # tab---tab 不好用
    # action_chains.key_down(Keys.TAB).key_up(Keys.TAB).perform()
    # time.sleep(2)
    # 点击内容元素
    content_element = driver.find_element(By.XPATH, '//div[@class="DraftEditor-editorContainer"]//div[@class="public-DraftStyleDefault-block public-DraftStyleDefault-ltr"]')
    content_element.click()
    time.sleep(2)
    # 模拟实际的粘贴操作
    action_chains.key_down(cmd_ctrl).send_keys('v').key_up(cmd_ctrl).perform()
    time.sleep(3)  # 等待5秒 不需要进行图片解析

    # 添加封面
    # TODO

    # 投稿至问题

    # 文章话题
    # TODO

    # 专栏收录

    # 确认发布
    confirm_button = driver.find_element(By.XPATH, '//button[contains(text(), "发布")]')
    # confirm_button.click()

    time.sleep(2)
