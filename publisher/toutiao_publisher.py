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

from publisher.common_handler import wait_login
from utils.file_utils import read_file_with_footer, convert_md_to_html, read_file, parse_front_matter
from utils.selenium_utils import get_html_web_content
from utils.yaml_file_utils import read_jianshu, read_common, read_segmentfault, read_oschina, read_zhihu, read_51cto, \
    read_infoq, read_txcloud, read_alcloud, read_toutiao
import time


def toutiao_publisher(driver,content=None):
    toutiao_config = read_toutiao()
    common_config = read_common()
    if content:
        common_config['content'] = content

    # 提取markdown文档的front matter内容：
    front_matter = parse_front_matter(common_config['content'])

    auto_publish = common_config['auto_publish']

    # 打开新标签页并切换到新标签页
    driver.switch_to.new_window('tab')
    # 浏览器实例现在可以被重用，进行你的自动化操作
    driver.get(toutiao_config['site'])
    time.sleep(2)  # 等待2秒

    # 文章标题
    wait_login(driver, By.XPATH, '//div[@class="publish-editor-title-inner"]//textarea[contains(@placeholder,"请输入文章标题")]')
    title = driver.find_element(By.XPATH, '//div[@class="publish-editor-title-inner"]//textarea[contains(@placeholder,"请输入文章标题")]')
    title.clear()
    if 'title' in front_matter and front_matter['title']:
        title.send_keys(front_matter['title'])
    else:
        title.send_keys(common_config['title'])
    time.sleep(2)  # 等待3秒

    # 文章内容 html版本
    content_file = common_config['content']
    content_file_html = convert_md_to_html(content_file)
    get_html_web_content(driver, content_file_html)
    time.sleep(2)  # 等待2秒
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(1)  # 等待1秒
    # 用tab定位，然后拷贝
    cmd_ctrl = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL
    # 模拟实际的粘贴操作（在某些情况下可能更合适）：
    action_chains = webdriver.ActionChains(driver)
    # action_chains.key_down(Keys.TAB).key_up(Keys.TAB).perform()
    # time.sleep(2)
    # print(pyperclip.paste())
    # 定位到要粘贴的位置
    content_element = driver.find_element(By.XPATH, '//div[@class="publish-editor"]//div[@class="ProseMirror"]')
    content_element.click()
    time.sleep(1)
    action_chains.key_down(cmd_ctrl).send_keys('v').key_up(cmd_ctrl).perform()
    time.sleep(3)  # 等待3秒

    # 标题设置
    # title = common_config['title']
    # if title:

    # 展示封面
    # TODO

    # 摘要
    if 'description' in front_matter and front_matter['description']:
        summary = front_matter['description']
    else:
        summary = common_config['summary']
    if summary:
        summary_input = driver.find_element(By.XPATH, '//div[@class="multi-abstract-cell-content-input"]//textarea[contains(@placeholder,"好的摘要比标题更吸引读者")]')
        summary_input.send_keys(summary)
    time.sleep(2)

    # 投放广告
    # TODO

    # 原创首发
    original_button = driver.find_element(By.XPATH, '//div[@class="original-tag"]//span[contains(text(),"声明原创")]')
    original_button.click()
    time.sleep(2)

    # 合集
    # TODO

    # 发布
    if auto_publish:
        publish_button = driver.find_element(By.XPATH, '//div[contains(@class,"publish-btn-last")]')
        publish_button.click()
