import sys
import time

from selenium.webdriver import Keys, ActionChains



def open_all_sites(driver):
    print("")


# 把html内容拷贝到剪贴板
def get_html_web_content(driver, html_file):
    # 打开新标签页并切换到新标签页
    driver.switch_to.new_window('tab')
    driver.get('file://' + html_file)
    time.sleep(1)
    # 获取页面的所有内容
    cmd_ctrl = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL

    ActionChains(driver) \
        .key_down(cmd_ctrl) \
        .send_keys("a") \
        .key_up(cmd_ctrl) \
        .key_down(cmd_ctrl) \
        .send_keys("c") \
        .key_up(cmd_ctrl) \
        .perform()

    # 关闭WebDriver会话
    driver.close()
    # 打印提示信息
    print("页面内容已复制到剪贴板。")