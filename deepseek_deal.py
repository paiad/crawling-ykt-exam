import pandas as pd

from tools.private_key import API_KEY
from tools.utils import save_to_file

exam_id = pd.read_csv('exam_id.csv')['exam_id'].iloc[0]

# 打开文件并读取内容
with open("./txt/雨课堂测试-id-{}.txt".format(exam_id), 'r', encoding='utf-8') as file:
    content = file.read()

from openai import OpenAI

# API_KEY 修改为自己的api_key密钥
client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "请依次回答这些问题" + content},
        # {"role": "user", "content": "hello"},
    ],
    stream=True
)

# 流式输出
# 先把所有流式输出内容收集到一个变量中
full_content = ""
for chunk in response:
    if chunk.choices[0].delta.content:
        full_content += chunk.choices[0].delta.content
        print(chunk.choices[0].delta.content, end='')

# 写入文件
save_to_file(full_content, filename="./txt/雨课堂测试-id-{}.txt".format(exam_id))




"""
# stream=False

ans = response.choices[0].message.content
print(ans)
"""