import json
import sys
import pyperclip

from selenium.webdriver import Keys, ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.wait import WebDriverWait

from utils.file_utils import read_file_with_footer
from utils.yaml_file_utils import read_jianshu, read_common, read_juejin
import time


def juejin_publisher(driver):
    juejin_config = read_juejin()
    common_config = read_common()

    # 打开新标签页并切换到新标签页
    driver.switch_to.new_window('tab')

    # 浏览器实例现在可以被重用，进行你的自动化操作
    driver.get(juejin_config['site'])
    time.sleep(2)  # 等待2秒

    # 设置等待
    wait = WebDriverWait(driver, 5)

    # 写文章按钮
    write_btn = driver.find_element(By.CLASS_NAME, 'send-button')
    write_btn.click()
    time.sleep(2)  # 等待3秒

    # 切换到新的tab
    driver.switch_to.window(driver.window_handles[-1])
    # 等待新标签页完成加载内容
    wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="输入文章标题..."]')))

    # 文章内容
    file_content = read_file_with_footer(common_config['content'])
    # 掘金比较特殊，不能用元素赋值的方法，所以我们使用拷贝的方法
    cmd_ctrl = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL
    # 将要粘贴的文本内容复制到剪贴板
    pyperclip.copy(file_content)
    content = driver.find_element(By.XPATH, '//div[@class="CodeMirror-code"]//span[@role="presentation"]')
    # print(content.get_attribute("innerHTML"))
    content.click()
    # 模拟实际的粘贴操作（在某些情况下可能更合适）：
    action_chains = webdriver.ActionChains(driver)
    action_chains.key_down(cmd_ctrl).send_keys('v').key_up(cmd_ctrl).perform()
    time.sleep(15)  # 等待15秒 图片解析需要花比较长时间

    # 文章标题
    title = driver.find_element(By.XPATH, '//input[@placeholder="输入文章标题..."]')
    title.clear()
    title.send_keys(common_config['title'])
    time.sleep(2)  # 等待3秒

    # 发布按钮
    publish_button = driver.find_element(By.XPATH, '//button[contains(text(), "发布")]')
    publish_button.click()
    time.sleep(2)

    # 发布文章 title
    title_label = driver.find_element(By.XPATH, '//div[contains(@class,"title") and contains(text(), "发布文章")]')

    # 分类
    category = juejin_config['category']
    if category:
        # print(category)
        category_btn = driver.find_element(By.XPATH, f'//div[@class="form-item-content category-list"]//div[contains(text(), "{category}")]')
        # print(category_btn.get_attribute("innerHTML"))
        category_btn.click()
        time.sleep(2)

    # 添加标签
    tag_btn = driver.find_element(By.XPATH, '//div[contains(@class,"byte-select__placeholder") and contains(text(), "请搜索添加标签")]')
    tag_btn.click()
    tags = juejin_config['tags']
    for tag in tags:
        # 使用复制粘贴的方式
        pyperclip.copy(tag)
        action_chains = webdriver.ActionChains(driver)
        action_chains.key_down(cmd_ctrl).send_keys('v').key_up(cmd_ctrl).perform()
        # 回车
        # action_chains.key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
        # 从下拉框中选择对应的tag
        tag_element = driver.find_element(By.XPATH, f'//li[contains(@class,"byte-select-option") and contains(text(), "{tag}")]')
        tag_element.click()
        time.sleep(2)  # 等待3秒

    title_label.click()

    # 文章封面
    # TODO

    # 收录至专栏
    collections = juejin_config['collections']
    collection_button = driver.find_element(By.XPATH, '//div[contains(@class,"byte-select__placeholder") and contains(text(), "请搜索添加专栏，同一篇文章最多添加三个专栏")]')
    collection_button.click()
    for coll in collections:
        # 使用复制粘贴的方式
        pyperclip.copy(coll)
        action_chains = webdriver.ActionChains(driver)
        action_chains.key_down(cmd_ctrl).send_keys('v').key_up(cmd_ctrl).perform()
        # 回车
        # action_chains.key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
        # 从下拉框中选择对应的tag
        coll_element = driver.find_element(By.XPATH, f'//li[contains(@class,"byte-select-option") and contains(text(), "{coll}")]')
        coll_element.click()
        time.sleep(2)  # 等待3秒

    title_label.click()

    # 创作话题
    topic = juejin_config['topic']
    if topic:
        topic_btn = driver.find_element(By.XPATH, '//div[contains(@class,"byte-select__placeholder") and contains(text(), "请搜索添加话题，最多添加1个话题")]')
        topic_btn.click()
        # 使用复制粘贴的方式
        pyperclip.copy(topic)
        action_chains = webdriver.ActionChains(driver)
        action_chains.key_down(cmd_ctrl).send_keys('v').key_up(cmd_ctrl).perform()
        # 从下拉框中选择对应的tag
        topic_element = driver.find_element(By.XPATH, f'//li[@class="byte-select-option"]//span[contains(text(), "{topic}")]')
        topic_element.click()
        time.sleep(2)  # 等待3秒

    title_label.click()

    # 编辑摘要
    summary = common_config['summary']
    if summary:
        summary_ui = driver.find_element(By.XPATH, '//textarea[@class="byte-input__textarea"]')
        summary_ui.clear()
        summary_ui.send_keys(summary)
        time.sleep(2)  # 等待3秒

    # 最终发布
    publish_button = driver.find_element(By.XPATH, '//button[contains(text(), "确定并发布")]')
    # publish_button.click()

