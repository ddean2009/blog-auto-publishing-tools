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

from utils.file_utils import read_file_with_footer, convert_md_to_html, read_file, parse_front_matter, download_image
from utils.selenium_utils import get_html_web_content
from utils.yaml_file_utils import read_jianshu, read_common, read_segmentfault, read_oschina, read_zhihu, read_mpweixin
import time


def mpweixin_publisher(driver,content=None):
    mpweixin_config = read_mpweixin()
    common_config = read_common()
    if content:
        common_config['content'] = content

    # 提取markdown文档的front matter内容：
    front_matter = parse_front_matter(common_config['content'])

    auto_publish = common_config['auto_publish']

    # driver.switch_to.window(driver.window_handles[0])
    # 打开新标签页并切换到新标签页
    driver.switch_to.new_window('tab')

    # 浏览器实例现在可以被重用，进行你的自动化操作
    driver.get(mpweixin_config['site'])
    time.sleep(2)  # 等待2秒

    # 点击图文消息
    pic_and_article_button = driver.find_element(By.XPATH,
                                                 '//div[@class="new-creation__menu-item"]//div[@class="new-creation__menu-title" and contains(text(), "图文消息")]')
    pic_and_article_button.click()
    time.sleep(1)

    # 切换到新的tab
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(1)

    # 文章标题
    title = driver.find_element(By.ID, 'title')
    title.clear()
    if 'title' in front_matter and front_matter['title']:
        title.send_keys(front_matter['title'])
    else:
        title.send_keys(common_config['title'])
    time.sleep(2)  # 等待3秒

    # 文章作者
    author = driver.find_element(By.ID, 'author')
    if 'authors' in front_matter and front_matter['authors']:
        author.send_keys(front_matter['authors'])
    else:
        author.send_keys(mpweixin_config['author'])
    time.sleep(1)

    # 文章内容 html版本
    content_file = common_config['content']
    # 注意，zhihu 不能识别转换过后的代码块格式
    content_file_html = convert_md_to_html(content_file, False)
    get_html_web_content(driver, content_file_html)
    time.sleep(2)  # 等待2秒
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(1)  # 等待1秒
    # 不能用元素赋值的方法，所以我们使用拷贝的方法
    cmd_ctrl = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL
    action_chains = webdriver.ActionChains(driver)
    # 点击内容元素
    content_element = driver.find_element(By.ID, 'edui1_contentplaceholder')
    ActionChains(driver).click(content_element).perform()
    # content_element.click()
    time.sleep(1)
    # 模拟实际的粘贴操作
    action_chains.key_down(cmd_ctrl).send_keys('v').key_up(cmd_ctrl).perform()
    time.sleep(3)  # 等待5秒 不需要进行图片解析

    # 添加封面
    # TODO

    # 原创声明
    original = mpweixin_config['original']
    if original:
        original_statement = driver.find_element(By.ID, 'js_original')
        original_statement.click()
        time.sleep(2)
        ## 点击确认按钮
        confirm_button = driver.find_element(By.XPATH,
                                             '//div[@class="weui-desktop-dialog"]//div[@class="weui-desktop-btn_wrp"]//button[contains(text(), "确定")]')
        confirm_button.click()
        time.sleep(1)
        # 赞赏
        zhanshang_button = driver.find_element(By.ID, 'js_reward_setting_area')
        zhanshang_button.click()
        time.sleep(1)
        ## 点击确认按钮
        confirm_button = driver.find_element(By.XPATH,
                                             '//div[@class="reward-setting-dialog__footer"]//div[@class="weui-desktop-btn_wrp"]//button[contains(text(), "确定")]')
        confirm_button.click()
        time.sleep(1)

    # 合集
    if 'tags' in front_matter and front_matter['tags']:
        tags = front_matter['tags']
    else:
        tags = mpweixin_config['tags']
    if tags:
        tag_button = driver.find_element(By.XPATH,
                                         '//div[@id="js_article_tags_area"]//div[contains(@class,"js_article_tags_label")]/span[text()="未添加"]')
        ActionChains(driver).scroll_by_amount(0, 400).perform()
        time.sleep(1)
        ActionChains(driver).move_to_element(tag_button).perform()
        time.sleep(1)
        ActionChains(driver).click(tag_button).perform()
        time.sleep(1)
        # 输入标签
        tag_input = driver.find_element(By.XPATH,
                                        '//span[@class="weui-desktop-form-tag__area"]//input[@placeholder="输入后按回车分割"]')
        for tag in tags:
            tag_input.send_keys(tag)
            time.sleep(1)
            tag_input.send_keys(Keys.ENTER)
            time.sleep(1)
        # 点击确定按钮
        confirm_button = driver.find_element(By.XPATH,
                                             '//div[@class="weui-desktop-btn_wrp"]//button[contains(text(), "确定")]')
        confirm_button.click()
        time.sleep(1)

    # 原文链接
    # TODO  感觉你们应该不需要这个功能

    # 确认发布
    if auto_publish:
        confirm_button = driver.find_element(By.ID, 'js_send')
        confirm_button.click()
        time.sleep(1)
        send_button = driver.find_element(By.XPATH, '//div[@class="weui-desktop-btn_wrp"]/button[text()="发表"]')
        # send_button.click()

    time.sleep(2)
