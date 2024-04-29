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

from utils.file_utils import read_file_with_footer
from utils.yaml_file_utils import read_jianshu, read_common, read_segmentfault, read_oschina, read_zhihu, read_51cto
import time


def cto51_publisher(driver):
    cto51_config = read_51cto()
    common_config = read_common()

    # 打开新标签页并切换到新标签页
    driver.switch_to.new_window('tab')

    # 浏览器实例现在可以被重用，进行你的自动化操作
    driver.get(cto51_config['site'])
    time.sleep(2)  # 等待2秒

    # 文章标题
    title = driver.find_element(By.ID, 'title')
    title.clear()
    title.send_keys(common_config['title'])
    time.sleep(2)  # 等待3秒

    # 文章内容 markdown版本
    file_content = read_file_with_footer(common_config['content'])
    # 找到初始的内容描述文字
    content = driver.find_element(By.XPATH, '//textarea[@placeholder="请输入正文"]')
    content.send_keys(file_content)
    time.sleep(15)  # 等待15秒 需要进行图片解析

    # 发布文章
    send_button = driver.find_element(By.XPATH, '//button[contains(@class, "edit-submit")]')
    # print(send_button.find_element(By.XPATH, '..').get_attribute('innerHTML'))
    # send_button.find_element(By.XPATH, '..').click()
    ActionChains(driver).click(send_button).perform()
    time.sleep(5)

    # 文章分类
    type = cto51_config['type']
    type_button = driver.find_element(By.XPATH, f'//div[@class="types-select-box"]//span[contains(text(),"{type}")]')
    type_button.click()
    time.sleep(2)

    # 个人分类
    # TODO
    # personal_type = cto51_config['personal_type']
    # personal_type_input = driver.find_element(By.ID, 'selfType')
    # personal_type_input.click()

    # 标签
    # TODO
    # tags = cto51_config['tags']
    # if tags:
    #     tag_input = driver.find_element(By.ID, 'tag-input')
    #     tag_input.clear()
    #     for tag in tags:
    #         tag_input.send_keys(tag)
    #         time.sleep(1)
    #         tag_input.send_keys(Keys.ENTER)

    # 摘要
    summary = common_config['summary']
    if summary:
        summary_input = driver.find_element(By.ID, 'abstractData')
        summary_input.clear()
        summary_input.send_keys(summary)

    # 话题
    topic = cto51_config['topic']
    if topic:
        topic_input = driver.find_element(By.ID, 'subjuct')
        topic_input.click()
        time.sleep(1)
        list_item_list = driver.find_element(By.ID, 'listItemList')
        list_item_list.find_element(By.XPATH, f'//li[contains(text(),"{topic}")]').click()

    # 发布
    publish_button = driver.find_element(By.ID, 'submitForm')
    # publish_button.click()









