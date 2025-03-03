# @Software  :PyCharm
# @Author    : ad
# @File      : file_transform.py
# @Time      : 2025-03-01 13:24
import pandas as pd
from tools.utils import txt_to_word

exam_id = pd.read_csv('exam_id.csv')['exam_id'].iloc[0]
# 示例调用
input_txt_path = "./txt/雨课堂测试-id-{}.txt".format(exam_id) # 输入的 .txt 文件路径
output_docx_path = './docs/雨课堂测试-id-{}.docx'.format(exam_id)  # 输出的 .docx 文件路径
txt_to_word(input_txt_path, output_docx_path)