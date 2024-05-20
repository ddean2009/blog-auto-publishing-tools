import time

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
from utils.yaml_file_utils import read_common
from publisher.jianshu_publisher import jianshu_publisher
from publisher.juejin_publisher import juejin_publisher

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

driver.implicitly_wait(15)  # 设置隐式等待时间为15秒

all_sites_home = {
    'csdn': 'https://www.csdn.net/',
    'jianshu': 'https://www.jianshu.com/',
    'juejin': 'https://juejin.cn/',
    'segmentfault': 'https://segmentfault.com/',
    'oschina': 'https://www.oschina.net/',
    'cnblogs': 'https://www.cnblogs.com/',
    'zhihu': 'https://www.zhihu.com/creator',
    'cto51': 'https://blog.51cto.com/flydean',
    'infoq': 'https://www.infoq.cn/',
    'txcloud': 'https://cloud.tencent.com/developer/support-plan',
    'alicloud': 'https://developer.aliyun.com/',
    'toutiao' : 'https://www.toutiao.com/',
    'mpweixin': 'https://mp.weixin.qq.com/'
}


def start_page(site_url, driver):
    # 打开新标签页并切换到新标签页
    driver.switch_to.new_window('tab')
    # 浏览器实例现在可以被重用，进行你的自动化操作
    driver.get(site_url)
    time.sleep(1)

def start_all_pages(driver):
    """
    发布到所有平台的封装函数
    """
    for site_home in all_sites_home:
        # print(site_home)
        if common_config['enable'][site_home]:
            # print(all_sites_home[site_home])
            start_page(all_sites_home[site_home], driver)
    # 在需要的时候关闭浏览器，不要关闭浏览器进程
    driver.quit()

if __name__ == '__main__':
    start_all_pages(driver)
