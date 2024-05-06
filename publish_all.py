import traceback

import selenium
from selenium import webdriver

from publisher.alicloud_publisher import alicloud_publisher
from publisher.cnblogs_publisher import cnblogs_publisher
from publisher.csdn_publisher import csdn_publisher
from publisher.cto51_publisher import cto51_publisher
from publisher.infoq_publisher import infoq_publisher
from publisher.oschina_publisher import oschina_publisher
from publisher.segmentfault_publisher import segmentfault_publisher
from publisher.toutiao_publisher import toutiao_publisher
from publisher.txcloud_publisher import txcloud_publisher
from publisher.zhihu_publisher import zhihu_publisher
from publisher.jianshu_publisher import jianshu_publisher
from publisher.juejin_publisher import juejin_publisher
from utils.yaml_file_utils import read_common

common_config = read_common()
driver_type= common_config['driver_type']
if driver_type == 'chrome':
    # 启动浏览器驱动服务
    service = selenium.webdriver.chrome.service.Service(common_config['service_location'])
    # Chrome 的调试地址
    debugger_address = common_config['debugger_address']
    # 创建Chrome选项，重用现有的浏览器实例
    options = selenium.webdriver.chrome.options.Options()
    options.page_load_strategy = 'normal'  # 设置页面加载策略为'normal' 默认值, 等待所有资源下载,
    options.add_experimental_option('debuggerAddress', debugger_address)
    # 使用服务和选项初始化WebDriver
    driver = webdriver.Chrome(service=service, options=options)
elif driver_type == 'firefox':
    # 启动浏览器驱动服务
    service = selenium.webdriver.firefox.service.Service(common_config['service_location'],
                                                         service_args=['--marionette-port', '2828',
                                                                       '--connect-existing'])
    # 创建firefox选项，重用现有的浏览器实例
    options = selenium.webdriver.firefox.options.Options()
    options.page_load_strategy = 'normal'  # 设置页面加载策略为'normal' 默认值, 等待所有资源下载,
    driver = webdriver.Firefox(service=service, options=options)

driver.implicitly_wait(10)  # 设置隐式等待时间为15秒

all_sites = ['csdn',
             'jianshu',
             'juejin',
             'segmentfault',
             'oschina',
             'cnblogs',
             'zhihu',
             'cto51',
             'infoq',
             'txcloud',
             'alicloud',
             'toutiao']


def publish_to_platform(platform, driver):
    """
    发布到指定平台的封装函数
    """
    try:
        globals()[platform + '_publisher'](driver)  # 动态调用对应平台的发布函数
    except Exception as e:
        print(platform,"got error")
        traceback.print_exc()  # 打印完整的异常跟踪信息
        print(e)


def publish_to_all_platforms(driver):
    """
    发布到所有平台的封装函数
    """
    for platform in all_sites:
        if platform in common_config['enable'] and common_config['enable'][platform]:
            publish_to_platform(platform, driver)
    # 在需要的时候关闭浏览器，不要关闭浏览器进程
    driver.quit()


# # 发布csdn
# if common_config['enable']['csdn']:
#     publish_to_platform('csdn', driver)
#
# # 发布简书
# if common_config['enable']['jianshu']:
#     publish_to_platform('jianshu', driver)
#
# # 发布掘金
# if common_config['enable']['juejin']:
#     publish_to_platform('juejin', driver)
#
# # 发布segmentfault
# if common_config['enable']['segmentfault']:
#     publish_to_platform('segmentfault', driver)
#
# # oschina
# if common_config['enable']['oschina']:
#     publish_to_platform('oschina', driver)
#
# # cnblogs
# if common_config['enable']['cnblogs']:
#     publish_to_platform('cnblogs', driver)
#
# # zhihu
# if common_config['enable']['zhihu']:
#     publish_to_platform('zhihu', driver)
#
# # 51cto
# if common_config['enable']['cto51']:
#     publish_to_platform('cto51', driver)
#
# # infoq
# if common_config['enable']['infoq']:
#     publish_to_platform('infoq', driver)
#
# # txcloud
# if common_config['enable']['txcloud']:
#     publish_to_platform('txcloud', driver)
#
# # alicloud
# if common_config['enable']['alicloud']:
#     publish_to_platform('alicloud', driver)
#
# # toutiao
# if common_config['enable']['toutiao']:
#     publish_to_platform('toutiao', driver)

if __name__ == '__main__':
    publish_to_all_platforms(driver)
    # publish_to_platform('zhihu', driver)
