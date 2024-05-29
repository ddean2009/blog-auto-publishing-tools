import sys

import pyperclip
from selenium.webdriver import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.wait import WebDriverWait

from publisher.common_handler import wait_login
from utils.file_utils import read_file_with_footer, parse_front_matter, download_image
from utils.yaml_file_utils import read_jianshu, read_common, read_segmentfault
import time


def segmentfault_publisher(driver,content=None):
    segmentfault_config = read_segmentfault()
    common_config = read_common()
    if content:
        common_config['content'] = content

    # 提取markdown文档的front matter内容：
    front_matter = parse_front_matter(common_config['content'])

    auto_publish = common_config['auto_publish']

    # 打开新标签页并切换到新标签页
    driver.switch_to.new_window('tab')
    # 浏览器实例现在可以被重用，进行你的自动化操作
    driver.get(segmentfault_config['site'])
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

    # 文章内容
    file_content = read_file_with_footer(common_config['content'])
    # segmentfault比较特殊，用的是CodeMirror,不能用元素赋值的方法，所以我们使用拷贝的方法
    cmd_ctrl = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL
    # 将要粘贴的文本内容复制到剪贴板
    pyperclip.copy(file_content)
    action_chains = webdriver.ActionChains(driver)
    # # 三次tab按钮，让光标定位到内容窗口：
    # for i in range(4):
    #     action_chains.key_down(Keys.TAB).key_up(Keys.TAB).perform()
    #     time.sleep(1)

    # 找到初始的内容描述文字
    # content = driver.find_element(By.XPATH, '//div[@class="CodeMirror-code"]//span[@role="presentation"]')
    content = driver.find_element(By.XPATH, '//div[@class="CodeMirror-code" and @role="presentation"]')
    # print(content.get_attribute("innerHTML"))
    action_chains.click(content).perform()
    # content.click()
    # 模拟实际的粘贴操作
    action_chains.key_down(cmd_ctrl).send_keys('v').key_up(cmd_ctrl).perform()
    time.sleep(3)  # 等待3秒



    # 添加标签
    tag_button = driver.find_element(By.ID, 'tags-toggle')
    tag_button.click()
    tag_input = driver.find_element(By.XPATH, '//input[@placeholder="搜索标签"]')
    if 'tags' in front_matter and front_matter['tags']:
        tag_list = front_matter['tags']
    else:
        tag_list = segmentfault_config['tags']
    for tag in tag_list:
        tag_input.clear()
        tag_input.send_keys(tag)
        tag_input.send_keys(Keys.ENTER)
        time.sleep(2)
    time.sleep(2)

    # # 发布按钮
    # publish_button = driver.find_element(By.ID, 'publish-toggle')
    # publish_button.click()
    # time.sleep(2)

    # 设置封面
    if 'image' in front_matter and front_matter['image']:
        file_input = driver.find_element(By.XPATH, "//input[@type='file']")
        # 文件上传不支持远程文件上传，所以需要把图片下载到本地
        file_input.send_keys(download_image(front_matter['image']))
        time.sleep(2)

    # 版权
    # copy_right = driver.find_element(By.ID, 'license')
    # copy_right.click()
    # time.sleep(2)

    # 确认发布
    if auto_publish:
        confirm_button = driver.find_element(By.ID, 'sureSubmitBtn')
        confirm_button.click()

    time.sleep(1)
