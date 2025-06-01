import re


# 保存文件
def save_to_file(data, filename="data.txt"):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(data + "\n\n")


# 使用正则表达式去除 HTML 标签
def remove_html_tags(text):
    clean_text = re.sub(r'<[^>]+>', '', text)
    return clean_text
