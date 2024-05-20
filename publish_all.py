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
from publisher.mpweixin_publisher import mpweixin_publisher
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
             'toutiao',
             'mpweixin']


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




if __name__ == '__main__':
    while True:
        print("选择你要发布的平台:\n")
        print("1. 全部")
        print("2. csdn")
        print("3. jianshu")
        print("4. juejin")
        print("5. segmentfault")
        print("6. oschina")
        print("7. cnblogs")
        print("8. zhihu")
        print("9. cto51")
        print("10. infoq")
        print("11. txcloud")
        print("12. alicloud")
        print("13. toutiao")
        print("14. mpweixin")
        print("0. 退出")

        choice = input("\n请选择: ")
        print("")

        if choice == '1':
            publish_to_all_platforms(driver)

        elif choice == '2':
            publish_to_platform('csdn', driver)

        elif choice == '3':
            publish_to_platform('jianshu', driver)

        elif choice == '4':
            publish_to_platform('juejin', driver)

        elif choice == '5':
            publish_to_platform('segmentfault', driver)

        elif choice == '6':
            publish_to_platform('oschina', driver)

        elif choice == '7':
            publish_to_platform('cnblogs', driver)

        elif choice == '8':
            publish_to_platform('zhihu', driver)

        elif choice == '9':
            publish_to_platform('cto51', driver)

        elif choice == '10':
            publish_to_platform('infoq', driver)

        elif choice == '11':
            publish_to_platform('txcloud', driver)

        elif choice == '12':
            publish_to_platform('alicloud', driver)

        elif choice == '13':
            publish_to_platform('toutiao', driver)

        elif choice == '14':
            publish_to_platform('mpweixin', driver)

        elif choice == '0':
            break

        else:
            print("无效的输入，请重新输入。")
