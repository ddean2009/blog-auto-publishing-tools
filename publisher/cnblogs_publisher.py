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
from utils.yaml_file_utils import read_jianshu, read_common, read_segmentfault, read_oschina, read_cnblogs
import time


def cnblogs_publisher(driver, content=None):
    cnblogs_config = read_cnblogs()
    common_config = read_common()
    if content:
        common_config['content'] = content
    print("content is :", common_config['content'])
    auto_publish = common_config['auto_publish']
    # 提取markdown文档的front matter内容：
    front_matter = parse_front_matter(common_config['content'])

    # 打开新标签页并切换到新标签页
    driver.switch_to.new_window('tab')

    # 浏览器实例现在可以被重用，进行你的自动化操作
    driver.get(cnblogs_config['site'])
    time.sleep(2)  # 等待2秒

    # 文章标题
    wait_login(driver, By.ID, 'post-title')
    title = driver.find_element(By.ID, 'post-title')
    title.clear()
    if 'title' in front_matter and front_matter['title']:
        title.send_keys(front_matter['title'])
    else:
        title.send_keys(common_config['title'])
    time.sleep(2)  # 等待2秒

    # 文章内容
    file_content = read_file_with_footer(common_config['content'])
    content = driver.find_element(By.ID, 'md-editor')
    content.send_keys(file_content)
    time.sleep(5)  # 等待2秒 不需要进行图片解析

    # 滚轮滚到最下面的位置
    submit_button = driver.find_element(By.XPATH, '//button[@data-el-locator="publishBtn"]')
    ActionChains(driver) \
        .scroll_to_element(submit_button) \
        .perform()
    time.sleep(1)

    # 个人分类
    categories = cnblogs_config['categories']
    if categories:
        post_category_select = driver.find_element(By.TAG_NAME, 'cnb-post-category-select')
        post_category_select.click()
        for category in categories:
            category_search = post_category_select.find_element(By.XPATH, '//nz-select-search/input')
            category_search.send_keys(category)
            time.sleep(1)
            category_select = post_category_select.find_element(By.XPATH, f'//nz-tree-node-title[contains(@title, "{category}")]/div')
            category_select.click()
            time.sleep(0.5)
        post_category_select.click()
    time.sleep(2)

    # 添加到合集
    collections = cnblogs_config['collections']
    if collections:
        collection_select = driver.find_element(By.NAME, '添加到合集')
        collection_select.click()
        # print(collection_select.get_attribute('innerHTML'))
        for collection in collections:
            collection_item = collection_select.find_element(By.XPATH, f'//span[contains(@class,"item__text") and contains(text(), "{collection}")]')
            parent_element = collection_item.find_element(By.XPATH, '..')
            # print(parent_element.tag_name)
            parent_element.click()
            time.sleep(0.5)
    time.sleep(2)

    # 投稿选项
    post_type = driver.find_element(By.ID, 'site-publish-site-home')
    post_type.click()
    time.sleep(2)

    # 投顾至网站分类
    topic = cnblogs_config['topic']
    if topic:
        post_type_detail = driver.find_element(By.NAME, '投稿至网站分类')
        post_type_detail.click()
        topic_item = driver.find_element(By.ID, topic)
        topic_item.click()
    time.sleep(2)

    # 摘要
    if 'description' in front_matter and front_matter['description']:
        summary = front_matter['description']
    else:
        summary = common_config['summary']
    summary_item = driver.find_element(By.ID, 'summary')
    summary_item.send_keys(summary)
    time.sleep(2)

    # tag标签
    tag_list = []
    if 'tags' in front_matter and front_matter['tags']:
        tag_list = front_matter['tags']
    else:
        tag_list = cnblogs_config['tags']
    if tag_list:
        tag_item = driver.find_element(By.ID, 'tags')
        tag_item.click()
        for tag in tag_list:
            tag_input = tag_item.find_element(By.TAG_NAME, 'input')
            tag_input.send_keys(tag)
            time.sleep(1)
            tag_input.send_keys(Keys.ENTER)
    time.sleep(2)

    # 提交文章
    if auto_publish:
        submit_button = driver.find_element(By.XPATH, '//button[@data-el-locator="publishBtn"]')
        submit_button.click()

