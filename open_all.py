import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

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
# 启动浏览器驱动服务
service = Service(common_config['service_location'])

# Chrome 的调试地址
debugger_address = common_config['debugger_address']

# 创建Chrome选项，重用现有的浏览器实例
options = Options()
options.page_load_strategy = 'normal'  # 设置页面加载策略为'normal' 默认值, 等待所有资源下载,
# options.page_load_strategy = 'eager' # 设置页面加载策略为'eager' 默认值, 不等待资源下载,
# options.page_load_strategy = 'none'  # 完全不会阻塞 WebDriver

# options.add_experimental_option("detach", True)  # 将 detach 参数设置为true将在驱动过程结束后保持浏览器的打开状态.
options.add_experimental_option('debuggerAddress', debugger_address)

# 使用服务和选项初始化WebDriver
driver = webdriver.Chrome(service=service, options=options)

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
    'toutiao' : 'https://www.toutiao.com/'
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
