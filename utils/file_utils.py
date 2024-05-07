import os
import re
import subprocess
from tempfile import gettempdir
from urllib.parse import urlparse

import requests
import yaml

from utils.yaml_file_utils import read_common

# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)

print("当前脚本的绝对路径是:", script_path)

# 脚本所在的目录
script_dir = os.path.dirname(script_path)
print("脚本所在的目录是:", script_dir)


def list_all_files(video_dir, extension='.mp4'):
    return_files = []
    for root, dirs, files in os.walk(video_dir):
        for file in files:
            if file.endswith(extension):
                return_files.append(os.path.join(root, file))
    return sorted(return_files)


def list_files(video_dir, extension='.mp4'):
    return_files = []
    for file in os.listdir(video_dir):
        if file.endswith(extension):
            return_files.append(os.path.join(video_dir, file))
    return sorted(return_files)


def read_head(file):
    with open(file, 'r', encoding='UTF-8') as file:
        # 读取文件内容
        head = file.readline()
        return head


# 读取第一行之后 添加一个回车，适用于第一行是文章标题的情况
def read_file_with_extra_enter(file):
    with open(file, 'r', encoding='UTF-8') as f:
        # 读取文件内容
        content = f.read()
        # 使用splitlines()将内容分割成行列表
        lines = content.splitlines()
        # 检查列表是否为空，并且只处理第一行（如果存在）
        if lines:
            # 在第一行末尾添加换行符（如果它不存在）
            if not lines[0].endswith('\n'):
                lines[0] += '\n'
        # 使用join()将行重新组合成字符串
        cleaned_content = '\n'.join(lines)
        return cleaned_content


def read_file(file):
    with open(file, 'r', encoding='UTF-8') as file:
        # 读取文件内容
        content = file.read()
        cleaned_content = remove_front_matter(content)
        cleaned_content = remove_truncate_content(cleaned_content)
        return cleaned_content


def read_file_all_content(file):
    with open(file, 'r', encoding='UTF-8') as file:
        # 读取文件内容
        content = file.read()
        cleaned_content = remove_truncate_content(content)
        return cleaned_content


def read_file_with_footer(file):
    with open(file, 'r') as file:
        # 读取文件内容
        content = file.read()
        cleaned_content = remove_front_matter(content)
        cleaned_content = remove_truncate_content(cleaned_content)
        common_config = read_common()
        if common_config['include_footer']:
            current_dir = os.getcwd()
            footer = read_file(os.path.join(current_dir, 'config/footer.md'))

        return cleaned_content + "\n" + footer


def remove_front_matter(markdown_content):
    # 正则表达式匹配front matter，假设它以'---'开始和结束
    front_matter_pattern = r'^---[\s\S]*?---'
    # 使用re.sub替换front matter为空字符串
    cleaned_content = re.sub(front_matter_pattern, '', markdown_content, flags=re.MULTILINE)
    return cleaned_content


def remove_truncate_content(content):
    # 删除blog中的  <!-- truncate --> 标签
    cleaned_content = content.replace("<!-- truncate -->", "")
    return cleaned_content


# 解析markdown中的front matter的内容
def parse_front_matter(content_file):
    metadata = []
    markdown_content = read_file_all_content(content_file)
    # 使用正则表达式匹配Front matter部分
    front_matter_pattern = re.compile(r'^---\n(.+?)\n---', re.DOTALL | re.MULTILINE)
    # 搜索并提取Front matter
    front_matter_match = front_matter_pattern.search(markdown_content)
    if front_matter_match:
        # 提取Front matter的内容
        front_matter_content = front_matter_match.group(1)
        # 使用yaml.safe_load解析YAML内容
        metadata = yaml.safe_load(front_matter_content)
        # print(metadata)
    else:
        print("没有找到Front matter部分。")
    return metadata


def convert_md_to_html(md_filename):
    # 获取文件名（不包含扩展名）和目录
    base_name = os.path.splitext(md_filename)[0]
    directory = os.path.dirname(md_filename)

    # 构建输出的HTML文件名
    html_filename = os.path.join(directory, base_name + '.html')

    # 如果HTML文件已经存在，直接返回
    if os.path.exists(html_filename):
        return html_filename

    # 同一目录下另一个文件的路径
    pandoc_css_path = os.path.join(script_dir, 'pandoc.css')

    # 构造pandoc命令
    command = ['pandoc', '--standalone', '--css', pandoc_css_path, '-f', 'markdown', '-t', 'html5', '--no-highlight',
               md_filename, '-o',
               html_filename]

    # 调用系统命令
    subprocess.run(command)

    common_config = read_common()
    if common_config['include_footer']:
        current_dir = os.getcwd()
        footer = os.path.join(current_dir, 'config/footer.html')

    # 把footer合并到html中
    # 打开两个文件：一个用于读取，另一个用于写入
    with open(footer, 'r') as source_file, open(html_filename, 'a') as destination_file:
        # 读取源文件的内容
        source_content = source_file.read()
        # 将读取的内容追加到目标文件的末尾
        destination_file.write(source_content)

    # 返回转换后的HTML文件名
    return html_filename


def download_image(url):
    # 检查URL是否以http开头
    if not url.startswith('http'):
        print("URL does not start with 'http'. Skipping download.")
        return url

    # 获取临时目录
    temp_dir = gettempdir()

    # 尝试解析URL
    try:
        parsed_url = urlparse(url)
        # 从URL中提取文件名
        filename = os.path.basename(parsed_url.path)
        # 完整的文件路径
        file_path = os.path.join(temp_dir, filename)

        # 发送GET请求
        response = requests.get(url, stream=True)

        # 检查请求是否成功
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:  # 过滤掉保持连接的chunk
                        f.write(chunk)
            print(f"Image downloaded to {file_path}")
            return file_path
        else:
            print(f"Failed to download image. HTTP Status Code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")
