import sys

import pyperclip
from selenium.webdriver import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.wait import WebDriverWait

from utils.file_utils import read_file_with_footer
from utils.yaml_file_utils import read_jianshu, read_common, read_segmentfault
import time


def segmentfault_publisher(driver):
    segmentfault_config = read_segmentfault()
    common_config = read_common()

    # 打开新标签页并切换到新标签页
    driver.switch_to.new_window('tab')
    # 浏览器实例现在可以被重用，进行你的自动化操作
    driver.get(segmentfault_config['site'])
    time.sleep(2)  # 等待2秒

    # 文章内容
    file_content = read_file_with_footer(common_config['content'])
    # segmentfault比较特殊，用的是CodeMirror,不能用元素赋值的方法，所以我们使用拷贝的方法
    cmd_ctrl = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL
    # 将要粘贴的文本内容复制到剪贴板
    pyperclip.copy(file_content)
    # 三次tab按钮，让光标定位到内容窗口：
    action_chains = webdriver.ActionChains(driver)
    for i in range(3):
        action_chains.key_down(Keys.TAB).key_up(Keys.TAB).perform()
        time.sleep(1)

    # 找到初始的内容描述文字
    content = driver.find_element(By.XPATH, '//div[@class="CodeMirror-code"]//span[@role="presentation"]')
    # print(content.get_attribute("innerHTML"))
    content.click()
    # 模拟实际的粘贴操作
    action_chains.key_down(cmd_ctrl).send_keys('v').key_up(cmd_ctrl).perform()
    time.sleep(3)  # 等待5秒 不需要进行图片解析

    # 文章标题
    title = driver.find_element(By.ID, 'title')
    title.clear()
    title.send_keys(common_config['title'])
    time.sleep(2)  # 等待3秒

    # 添加标签
    tag_button = driver.find_element(By.ID, 'tags-toggle')
    tag_button.click()
    tag_input = driver.find_element(By.XPATH, '//input[@placeholder="搜索标签"]')
    for tag in segmentfault_config['tags']:
        tag_input.send_keys(tag)
        tag_input.send_keys(Keys.ENTER)
        time.sleep(2)
    time.sleep(2)

    # 发布按钮
    publish_button = driver.find_element(By.ID, 'publish-toggle')
    publish_button.click()
    time.sleep(2)

    # 设置封面
    # TODO
    # upload_file = common_config['cover']
    # file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    # file_input.send_keys(upload_file)
    # driver.find_element(By.ID, "file-submit").click()

    # 版权
    # copy_right = driver.find_element(By.ID, 'license')
    # copy_right.click()
    # time.sleep(2)

    # 确认发布
    confirm_button = driver.find_element(By.ID, 'sureSubmitBtn')
    # confirm_button.click()

    time.sleep(1)
