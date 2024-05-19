import yaml
import os


def read_yaml(file, encoding='UTF-8'):
    """
    读取并解析 YAML 格式的配置文件。

    参数:
    file: 字符串，表示需要读取的 YAML 文件的路径。

    返回值:
    读取并解析后的数据，数据类型取决于 YAML 文件的内容。

    异常:
    如果遇到 YAML 解析错误，将打印错误信息。
    """
    with open(file, 'r', encoding=encoding) as stream:  # 打开文件并以读取模式进行处理
        try:
            data = yaml.safe_load(stream)  # 安全地解析 YAML 格式的文件内容
            return data
        except yaml.YAMLError as exc:  # 捕获并处理 YAML 解析错误
            print(exc)


def read_common():
    """
    读取通用配置文件。

    该函数没有参数。

    返回:
        返回从通用配置文件中读取的数据。
    """
    # 获取当前工作目录
    current_dir = os.getcwd()
    return read_yaml(os.path.join(current_dir, 'config/common.yaml'))  # 读取并返回配置文件中的数据

def read_common_video():
    """
    读取通用配置文件。

    该函数没有参数。

    返回:
        返回从通用配置文件中读取的数据。
    """
    # 获取当前工作目录
    current_dir = os.getcwd()
    return read_yaml(os.path.join(current_dir, 'config/common_video.yaml'))  # 读取并返回配置文件中的数据

def read_common_video_firefox():
    """
    读取通用配置文件。

    该函数没有参数。

    返回:
        返回从通用配置文件中读取的数据。
    """
    # 获取当前工作目录
    current_dir = os.getcwd()
    return read_yaml(os.path.join(current_dir, 'config/common_video_firefox_english.yaml'))  # 读取并返回配置文件中的数据


def read_jianshu():
    """
    读取简书配置文件。

    该函数没有参数。

    返回:
        返回从简书配置文件中读取的数据。
    """
    current_dir = os.getcwd()
    return read_yaml(os.path.join(current_dir, 'config/jianshu.yaml'))

def read_xiaohongshu():
    current_dir = os.getcwd()
    return read_yaml(os.path.join(current_dir, 'config/xiaohongshu.yaml'))

def read_douyin():
    current_dir = os.getcwd()
    return read_yaml(os.path.join(current_dir, 'config/douyin.yaml'))


def read_kuaishou():
    current_dir = os.getcwd()
    return read_yaml(os.path.join(current_dir, 'config/kuaishou.yaml'))

def read_shipinhao():
    current_dir = os.getcwd()
    return read_yaml(os.path.join(current_dir, 'config/shipinhao.yaml'))


def read_zhihu():
    """
    读取知乎配置文件。

    该函数没有参数。

    返回:
        返回从知乎配置文件中读取的数据。
    """
    current_dir = os.getcwd()
    return read_yaml(os.path.join(current_dir, 'config/zhihu.yaml'))


def read_juejin():
    """
    读取掘金配置文件。

    该函数没有参数。

    返回:
        返回从掘金配置文件中读取的数据。
    """
    current_dir = os.getcwd()
    return read_yaml(os.path.join(current_dir, 'config/juejin.yaml'))


def read_segmentfault():
    current_dir = os.getcwd()
    return read_yaml(os.path.join(current_dir, 'config/segmentfault.yaml'))


def read_oschina():
    current_dir = os.getcwd()
    return read_yaml(os.path.join(current_dir, 'config/oschina.yaml'))

def read_mpweixin():
    current_dir = os.getcwd()
    return read_yaml(os.path.join(current_dir, 'config/mpweixin.yaml'))


def read_cnblogs():
    current_dir = os.getcwd()
    return read_yaml(os.path.join(current_dir, 'config/cnblogs.yaml'))


def read_zhihu():
    current_dir = os.getcwd()
    return read_yaml(os.path.join(current_dir, 'config/zhihu.yaml'))


def read_51cto():
    current_dir = os.getcwd()
    return read_yaml(os.path.join(current_dir, 'config/51cto.yaml'))


def read_infoq():
    current_dir = os.getcwd()
    return read_yaml(os.path.join(current_dir, 'config/infoq.yaml'))


def read_txcloud():
    current_dir = os.getcwd()
    return read_yaml(os.path.join(current_dir, 'config/txcloud.yaml'))


def read_alcloud():
    current_dir = os.getcwd()
    return read_yaml(os.path.join(current_dir, 'config/alicloud.yaml'))


def read_toutiao():
    current_dir = os.getcwd()
    return read_yaml(os.path.join(current_dir, 'config/toutiao.yaml'))


def read_csdn():
    """
    读取 CSDN 配置文件。

    该函数没有参数。

    返回:
        返回从 CSDN 配置文件中读取的数据。
    """
    current_dir = os.getcwd()
    return read_yaml(os.path.join(current_dir, 'config/csdn.yaml'))
