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
from utils.file_utils import read_file_with_footer, read_file, parse_front_matter, download_image
from utils.yaml_file_utils import read_jianshu, read_common, read_segmentfault, read_oschina, read_zhihu, read_51cto, \
    read_infoq, read_txcloud
import time


def txcloud_publisher(driver,content=None):
    txcloud_config = read_txcloud()
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
    driver.get(txcloud_config['site'])
    time.sleep(2)  # 等待2秒

    wait_login(driver, By.XPATH,
               '//div[@class="col-editor-switch"]//a')

    # 切换到markdown编辑器
    a_switch = driver.find_element(By.XPATH, '//div[@class="col-editor-switch"]//a')
    # 获取a元素的文本内容
    text_content = a_switch.text
    if text_content == '切换到Markdown编辑器':
        a_switch.click()
    time.sleep(2)

    # 文章标题
    title = driver.find_element(By.XPATH, '//textarea[@placeholder="请输入标题"]')
    title.clear()
    if 'title' in front_matter and front_matter['title']:
        title.send_keys(front_matter['title'])
    else:
        title.send_keys(common_config['title'])
    time.sleep(2)  # 等待3秒

    # 文章内容 markdown版本, 腾讯云不能有引流链接
    file_content = read_file(common_config['content'])
    # 用的是CodeMirror,不能用元素赋值的方法，所以我们使用拷贝的方法
    cmd_ctrl = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL
    # 将要粘贴的文本内容复制到剪贴板
    pyperclip.copy(file_content)
    action_chains = webdriver.ActionChains(driver)
    content = driver.find_element(By.XPATH, '//div[contains(@class,"draft-markdown-editor")]//div[@class="view-line"]')
    content.click()
    time.sleep(2)
    # 模拟实际的粘贴操作
    action_chains.key_down(cmd_ctrl).send_keys('v').key_up(cmd_ctrl).perform()
    time.sleep(3)  # 等待3秒

    # 发布文章
    send_button = driver.find_element(By.XPATH, '//button[contains(@class, "c-btn") and contains(text(),"发布")]')
    send_button.click()
    # ActionChains(driver).click(send_button).perform()
    time.sleep(2)

    # 文章来源
    source = driver.find_element(By.XPATH, '//ul[@class="com-check-list"]/li/label/span[contains(text(),"原创")]')
    source.click()
    time.sleep(2)

    # 文章分类
    article_type = txcloud_config['article_type']
    if article_type:
        article_type_select = driver.find_element(By.XPATH, '//section[@class="col-editor-sidebar publish"]//div[@class="tea-dropdown col-editor-classify"]/div')
        article_type_select.click()
        time.sleep(1)
        article_type_element = driver.find_element(By.XPATH,f'//div[@class="tea-dropdown-box"]//ul//li//label//span[text()="{article_type}"]')
        article_type_element.click()
        time.sleep(1)
    # 文章分类label
    article_type_label = driver.find_element(By.XPATH, '//label[@class="c-f-list-tit" and text()="文章分类"]')
    ActionChains(driver).click(article_type_label).perform()
    time.sleep(1)

    # 文章标签
    if 'tags' in front_matter and front_matter['tags']:
        tags = front_matter['tags']
    else:
        tags = txcloud_config['tags']
    if tags:
        tag_label = driver.find_element(By.XPATH,
                                        '//div[@class="com-2-tag-cont"]/label[contains(text(),"搜索并选择合适的标签")]')
        tag_input = tag_label.find_element(By.XPATH, '../input[@class="com-2-tag-input"]')
        for tag in tags:
            tag_input.send_keys(tag)
            time.sleep(1)
            tag_input.send_keys(Keys.ENTER)
            time.sleep(1)

    # 关键词
    keywords = txcloud_config['keywords']
    if keywords:
        for keyword in keywords:
            keyword_input = driver.find_element(By.XPATH,
                                                '//div[@class="col-editor-key-input"]//div[@class="com-2-tag-cont"]/input[@class="com-2-tag-input"]')

            keyword_input.send_keys(keyword)
            time.sleep(1)
            keyword_input.send_keys(Keys.ENTER)
            time.sleep(1)

    # 专栏
    zhuanlan = txcloud_config['zhuanlan']
    if zhuanlan:
        zhuanlan_element = driver.find_element(By.XPATH, f'//span[@class="col-editor-create-name" and contains(text(),"{zhuanlan}")]')
        zhuanlan_element.click()

    # 文章封面
    # if 'image' in front_matter and front_matter['image']:
    #     file_input = driver.find_element(By.ID, "editor-upload-input")
    #     # 文件上传不支持远程文件上传，所以需要把图片下载到本地
    #     file_input.send_keys(download_image(front_matter['image']))
    #     time.sleep(2)

    # 发布
    if auto_publish:
        publish_button = driver.find_element(By.XPATH, '//div[contains(@class,"block c-btn") and contains(text(),"确认发布")]')
        publish_button.click()
