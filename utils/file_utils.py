import os
import re
import subprocess

from utils.yaml_file_utils import read_common


def read_file(file):
    with open(file, 'r') as file:
        # 读取文件内容
        content = file.read()
        cleaned_content = remove_front_matter(content)
        return cleaned_content


def read_file_with_footer(file):
    with open(file, 'r') as file:
        # 读取文件内容
        content = file.read()
        cleaned_content = remove_front_matter(content)
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


def convert_md_to_html(md_filename):
    # 获取文件名（不包含扩展名）和目录
    base_name = os.path.splitext(md_filename)[0]
    directory = os.path.dirname(md_filename)

    # 构建输出的HTML文件名
    html_filename = os.path.join(directory, base_name + '.html')

    # 如果HTML文件已经存在，直接返回
    if os.path.exists(html_filename):
        return html_filename

    # 构造pandoc命令
    command = ['pandoc', md_filename, '-o', html_filename]

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
