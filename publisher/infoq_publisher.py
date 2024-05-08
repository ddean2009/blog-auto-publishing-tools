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

from utils.file_utils import read_file_with_footer, parse_front_matter, download_image
from utils.yaml_file_utils import read_jianshu, read_common, read_segmentfault, read_oschina, read_zhihu, read_51cto, \
    read_infoq
import time


def infoq_publisher(driver):
    infoq_config = read_infoq()
    common_config = read_common()

    # 提取markdown文档的front matter内容：
    front_matter = parse_front_matter(common_config['content'])
    auto_publish = common_config['auto_publish']

    # 打开新标签页并切换到新标签页
    driver.switch_to.new_window('tab')

    # 浏览器实例现在可以被重用，进行你的自动化操作
    driver.get(infoq_config['site'])
    time.sleep(2)  # 等待2秒

    # 点击立即创作按钮
    create_button = driver.find_element(By.XPATH, '//div[contains(@class, "write-btn")]')
    create_button.click()
    time.sleep(2)
    # 切换到新的tab
    driver.switch_to.window(driver.window_handles[-1])

    # 上传封面
    if 'image' in front_matter and front_matter['image']:
        file_input = driver.find_element(By.XPATH, "//input[@type='file']")
        # 文件上传不支持远程文件上传，所以需要把图片下载到本地
        file_input.send_keys(download_image(front_matter['image']))
        time.sleep(2)

    # 文章标题
    title = driver.find_element(By.XPATH, '//input[@placeholder="请输入标题"]')
    title.clear()
    if 'title' in front_matter['title'] and front_matter['title']:
        title.send_keys(front_matter['title'])
    else:
        title.send_keys(common_config['title'])
    time.sleep(2)  # 等待3秒

    # 文章内容 markdown版本
    file_content = read_file_with_footer(common_config['content'])
    # 用的是CodeMirror,不能用元素赋值的方法，所以我们使用拷贝的方法
    cmd_ctrl = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL
    # 将要粘贴的文本内容复制到剪贴板
    pyperclip.copy(file_content)
    action_chains = webdriver.ActionChains(driver)
    # tab
    action_chains.key_down(Keys.TAB).key_up(Keys.TAB).perform()
    time.sleep(2)
    # 模拟实际的粘贴操作
    action_chains.key_down(cmd_ctrl).send_keys('v').key_up(cmd_ctrl).perform()
    time.sleep(3)  # 等待3秒

    # 发布文章
    send_button = driver.find_element(By.XPATH, '//div[contains(@class, "submit-btn")]')
    # print(send_button.find_element(By.XPATH, '..').get_attribute('innerHTML'))
    send_button.click()
    # ActionChains(driver).click(send_button).perform()
    time.sleep(2)

    # 摘要
    if 'description' in front_matter['description'] and front_matter['description']:
        summary = front_matter['description']
    else:
        summary = common_config['summary']
    if summary:
        summary_input = driver.find_element(By.XPATH, '//div[@class="summary"]/textarea')
        summary_input.clear()
        summary_input.send_keys(summary)
    time.sleep(2)

    # 标签
    tags = infoq_config['tags']
    if tags:
        for tag in tags:
            tag_input = driver.find_element(By.XPATH, '//div[@class="search-tag"]//input')
            tag_input.send_keys(tag)
            time.sleep(1)
            tag_input.send_keys(Keys.ENTER)

    # 发布
    if auto_publish:
        publish_button = driver.find_element(By.XPATH, '//div[@class="dialog-footer-buttons"]/div[contains(text(),"确定")]')
        publish_button.click()









