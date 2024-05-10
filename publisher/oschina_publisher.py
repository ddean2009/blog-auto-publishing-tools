import sys

import pyperclip
from selenium.webdriver import Keys, ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

from utils.file_utils import read_file_with_footer, parse_front_matter
from utils.yaml_file_utils import read_jianshu, read_common, read_segmentfault, read_oschina
import time


def oschina_publisher(driver):
    oschina_config = read_oschina()
    common_config = read_common()
    auto_publish = common_config['auto_publish']

    # 提取markdown文档的front matter内容：
    front_matter = parse_front_matter(common_config['content'])

    # driver.switch_to.window(driver.window_handles[0])

    # 打开新标签页并切换到新标签页
    driver.switch_to.new_window('tab')

    # 浏览器实例现在可以被重用，进行你的自动化操作
    driver.get(oschina_config['site'])
    time.sleep(2)  # 等待2秒

    # 文章内容
    file_content = read_file_with_footer(common_config['content'])
    # 用的是CodeMirror,不能用元素赋值的方法，所以我们使用拷贝的方法
    cmd_ctrl = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL
    # 将要粘贴的文本内容复制到剪贴板
    pyperclip.copy(file_content)
    action_chains = webdriver.ActionChains(driver)

    # 找到初始的内容描述文字
    content = driver.find_element(By.XPATH, '//div[@class="CodeMirror-code"]//span[@role="presentation"]')
    # print(content.get_attribute("innerHTML"))
    content.click()
    # 模拟实际的粘贴操作
    action_chains.key_down(cmd_ctrl).send_keys('v').key_up(cmd_ctrl).perform()
    time.sleep(3)  # 等待3秒

    # 文章标题
    title = driver.find_element(By.NAME, 'title')
    title.clear()
    if 'title' in front_matter['title'] and front_matter['title']:
        title.send_keys(front_matter['title'])
    else:
        title.send_keys(common_config['title'])
    time.sleep(2)  # 等待3秒

    # 发布按钮
    publish_button = driver.find_element(By.XPATH, '//div[contains(@class,"submit button") and contains(text(), "发布文章")]')
    publish_button.click()
    time.sleep(2)

    # 文章专辑
    collection = oschina_config['collection']
    if collection:
        category_select = driver.find_element(By.XPATH, '//div[contains(@class, "selection dropdown catalog-select")]')
        category_select.click()
        time.sleep(1)
        select_element = category_select.find_element(By.XPATH, f'//div[@class="item" and contains(text(), "{collection}")]')
        ActionChains(driver).move_to_element(select_element).perform()
        time.sleep(1)
        ActionChains(driver).click(select_element).perform()
        time.sleep(2)

    # 推广专区
    topic = oschina_config['topic']
    if topic:
        topic_select = driver.find_element(By.XPATH, '//div[contains(@class, "selection dropdown groups")]')
        topic_select.click()
        time.sleep(1)
        topic_item = topic_select.find_element(By.XPATH, f'//div[@class="item" and contains(text(), "{topic}")]')
        ActionChains(driver).move_to_element(topic_item).perform()
        time.sleep(1)
        ActionChains(driver).click(topic_item).perform()
        time.sleep(2)


    # 确认发布
    if auto_publish:
        confirm_button = driver.find_element(By.XPATH, '//div[contains(@class,"submit button effective-button")]')
        confirm_button.click()

    time.sleep(2)
