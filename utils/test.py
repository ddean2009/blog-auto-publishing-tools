import re
import string


def insert_newline(text):
    # 创建一个正则表达式，匹配任何标点符号
    punctuations = '[' + re.escape(string.punctuation) + ']'
    # 正则表达式匹配长度为30的字符串，后面紧跟空格或标点符号
    pattern = r'(.{10})(?=' + punctuations + r'|\s)'
    # 使用 re.sub 替换匹配的部分，在匹配到的字符串后添加换行符
    return re.sub(pattern, r'\1\n', text)

print(insert_newline("你好你好你好你好你好你好你好你好你好你好你好?你好你好你好你好你好你好"))
