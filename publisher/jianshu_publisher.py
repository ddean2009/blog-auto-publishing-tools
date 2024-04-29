from selenium.webdriver.common.by import By
from selenium.webdriver.support import wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.wait import WebDriverWait

from utils.file_utils import read_file_with_footer
from utils.yaml_file_utils import read_jianshu, read_common
import time


def jianshu_publisher(driver):
    jianshu_config = read_jianshu()
    common_config = read_common()

    # 打开新标签页并切换到新标签页
    driver.switch_to.new_window('tab')

    # 浏览器实例现在可以被重用，进行你的自动化操作
    driver.get(jianshu_config['site'])
    time.sleep(2)  # 等待2秒

    # 设置等待
    wait = WebDriverWait(driver, 5)

    # 存储原始窗口的 ID
    # original_window = driver.current_window_handle

    # 写文章按钮
    write_btn = driver.find_element(By.CLASS_NAME, 'write-btn')
    write_btn.click()
    time.sleep(2)  # 等待3秒

    # 等待新窗口或标签页
    # wait.until(EC.number_of_windows_to_be(2))

    # # 循环执行，直到找到一个新的窗口句柄
    # for window_handle in driver.window_handles:
    #     if window_handle != original_window:
    #         driver.switch_to.window(window_handle)
    #         break

    # 切换到新的tab
    driver.switch_to.window(driver.window_handles[-1])
    # 等待新标签页完成加载内容
    wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'li'), '日记本'))

    # 找到要发表的文集
    # 使用XPath表达式查找元素
    li_element = driver.find_element(By.XPATH, '//li[@title="AIGC"]')
    li_element.click()
    time.sleep(2)  # 等待3秒

    # 点击新建文章按钮
    new_article_btn = driver.find_element(By.CLASS_NAME, 'fa-plus-circle')
    new_article_btn.click()
    time.sleep(2)  # 等待3秒

    # 文章内容
    content = driver.find_element(By.ID, 'arthur-editor')
    file_content = read_file_with_footer(common_config['content'])
    content.clear()
    content.send_keys(file_content)
    time.sleep(2)  # 等待3秒

    # 文章标题
    title = driver.find_element(locate_with(By.TAG_NAME, "input").above({By.ID: "arthur-editor"}))
    title.clear()
    title.send_keys(common_config['title'])
    time.sleep(2)  # 等待3秒

    # 发布按钮
    publish_button = driver.find_element(By.XPATH, '//a[@data-action="publicize"]')

    publish_button.click()

    # 检查弹窗
    alert = wait.until(EC.text_to_be_present_in_element((By.XPATH, '//div[@role="document"]'), '有图片未上传成功'))
    if alert:
        ok_button = driver.find_element(locate_with(By.TAG_NAME, "button").near({By.XPATH: '//div[@role="document"]'}))
        ok_button.click()
        time.sleep(2)
        print("Alert accepted")
        # 重新发布一次
        publish_button.click()
    else:
        print("No alert found")

    time.sleep(2)
