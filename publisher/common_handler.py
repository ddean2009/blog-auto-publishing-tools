from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.yaml_file_utils import read_common


def wait_login(driver, element_type, element_value):
    common_config = read_common()
    if common_config["wait_login"]:
        print("等待用户登录")
        wait_login_time = common_config["wait_login_time"]
        try:
            # 设置显式等待的时间 默认120s
            wait = WebDriverWait(driver, wait_login_time)
            # 等待元素出现
            wait.until(EC.presence_of_element_located((element_type, element_value)))
        except Exception as e:
            print(e)
        print("等待登录结束")
