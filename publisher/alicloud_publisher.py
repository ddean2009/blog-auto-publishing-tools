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
from utils.file_utils import read_file_with_footer, parse_front_matter
from utils.yaml_file_utils import read_jianshu, read_common, read_segmentfault, read_oschina, read_zhihu, read_51cto, \
    read_infoq, read_txcloud, read_alcloud
import time


def alicloud_publisher(driver, content=None):
    alicloud_config = read_alcloud()
    common_config = read_common()
    if content:
        common_config['content'] = content
    auto_publish = common_config['auto_publish']
    # 提取markdown文档的front matter内容：
    front_matter = parse_front_matter(common_config['content'])

    # 打开新标签页并切换到新标签页
    driver.switch_to.new_window('tab')

    # 浏览器实例现在可以被重用，进行你的自动化操作
    driver.get(alicloud_config['site'])
    time.sleep(2)  # 等待2秒

    # 文章标题
    wait_login(driver, By.XPATH, '//input[@placeholder="请填写标题"]')
    title = driver.find_element(By.XPATH, '//input[@placeholder="请填写标题"]')
    title.clear()
    if 'title' in front_matter and front_matter['title']:
        title.send_keys(front_matter['title'])
    else:
        title.send_keys(common_config['title'])
    time.sleep(2)  # 等待3秒

    # 文章内容 markdown版本
    file_content = read_file_with_footer(common_config['content'])
    content = driver.find_element(By.XPATH, '//div[@class="editor"]//textarea[@class="textarea"]')
    content.send_keys(file_content)
    time.sleep(3)  # 等待3秒

    # 摘要
    if 'description' in front_matter and front_matter['description']:
        summary = front_matter['description']
    else:
        summary = common_config['summary']
    if summary:
        summary_input = driver.find_element(By.XPATH, '//div[@class="abstractContent-box"]//textarea[@placeholder="请填写摘要"]')
        summary_input.send_keys(summary)

    # 子社区
    # TODO

    # 设置封面
    # TODO 阿里云不支持input标签

    # 发布
    if auto_publish:
        publish_button = driver.find_element(By.XPATH, '//div[@class="publish-fixed-box-btn"]/button[contains(text(),"发布文章")]')
        publish_button.click()
