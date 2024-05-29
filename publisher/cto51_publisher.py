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
from utils.yaml_file_utils import read_jianshu, read_common, read_segmentfault, read_oschina, read_zhihu, read_51cto
import time


def cto51_publisher(driver,content=None):
    cto51_config = read_51cto()
    common_config = read_common()
    if content:
        common_config['content'] = content
    auto_publish = common_config['auto_publish']
    # 提取markdown文档的front matter内容：
    front_matter = parse_front_matter(common_config['content'])

    # driver.switch_to.window(driver.window_handles[0])

    # 打开新标签页并切换到新标签页
    driver.switch_to.new_window('tab')

    # 浏览器实例现在可以被重用，进行你的自动化操作
    driver.get(cto51_config['site'])
    time.sleep(2)  # 等待2秒

    # 文章标题
    wait_login(driver, By.ID, 'title')
    title = driver.find_element(By.ID, 'title')
    title.clear()
    if 'title' in front_matter and front_matter['title']:
        title.send_keys(front_matter['title'])
    else:
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
    ActionChains(driver).click(send_button).perform()
    time.sleep(5)

    # 文章分类
    type = cto51_config['type']
    type_button = driver.find_element(By.XPATH, f'//div[@class="types-select-box"]//span[contains(text(),"{type}")]')
    type_button.click()
    time.sleep(2)

    # 个人分类
    personal_type = cto51_config['personal_type']
    personal_type_input = driver.find_element(By.ID, 'selfType')
    personal_type_input.click()
    time.sleep(1)
    personal_type_element = driver.find_element(By.XPATH,f'//div[@class="el-select classification person-type"]//li[@class="el-select-dropdown__item"]/span[text()="{personal_type}"]')
    personal_type_element.click()
    time.sleep(1)

    # 标签
    if 'tags' in front_matter and front_matter['tags']:
        tags = front_matter['tags']
    else:
        tags = cto51_config['tags']
    if tags:
        print(tags)
        tag_input = driver.find_element(By.ID, 'tag-input')
        # 这个clear是没有用的
        # tag_input.clear()
        # 找到要操作的元素
        # tag_list_locator = locate_with(By.TAG_NAME, "div").above({By.ID: "tag-input"})
        tag_list_div = tag_input.find_element(By.XPATH, 'preceding-sibling::div')
        # 使用 JavaScript 删除子元素
        driver.execute_script("arguments[0].innerHTML = '';", tag_list_div)
        time.sleep(1)
        for tag in tags:
            print(tag)
            tag_input.send_keys(tag)
            time.sleep(1)
            tag_input.send_keys(Keys.ENTER)

    # 摘要
    if 'description' in front_matter and front_matter['description']:
        summary = front_matter['description']
    else:
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
    if auto_publish:
        publish_button = driver.find_element(By.ID, 'submitForm')
        publish_button.click()









