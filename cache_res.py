# @Software  :PyCharm
# @Author    : paiad
# @File      : commit.py
# @Time      : 2025-03-22 16:41
from mitmproxy import http
import pandas as pd
import json

from tools.utils import remove_html_tags, save_to_file


# 请求拦截和修改
def request(flow: http.HTTPFlow) -> None:
    """
    在请求到达目标服务器前，拦截并打印请求信息
    """
    target_url = "examination.xuetangx.com/exam"
    if target_url in flow.request.pretty_url:
        # 打印请求的基本信息
        print(f"\n=== New Request ===")
        print(f"URL: {flow.request.pretty_url}")
        print(f"Method: {flow.request.method}")
        print(f"Headers: {dict(flow.request.headers)}")

        # 如果有请求体，打印请求内容
        if flow.request.content:
            try:
                content = flow.request.content.decode('utf-8')
                print(f"Request Content: {content}")
            except:
                print(f"Request Content (raw): {flow.request.content}")


# 响应拦截和修改
def response(flow: http.HTTPFlow) -> None:
    """
    在响应返回给客户端前，拦截并打印响应信息
    """
    target_url = "https://examination.xuetangx.com/exam_room/cache_results?exam_id="
    exam_id = pd.read_csv('exam_id.csv')['exam_id'].iloc[0]
    target_url += str(exam_id)

    if target_url in flow.request.pretty_url:

        # 尝试解析和打印响应内容
        if flow.response.content:
            try:
                # 尝试解码为 UTF-8 并解析 JSON
                content = flow.response.content.decode('utf-8')
                try:
                    json_data = json.loads(content)
                    pretty_json = json.dumps(json_data, indent=2, ensure_ascii=False)
                    print("====================================================")
                    print(pretty_json)


                    cache = json_data["data"]["results"]
                    # 创建数据列表
                    data = []

                    for problem in cache:
                        data.append({
                            "problem_id": problem["problem_id"],
                            "result": problem["result"],
                        })
                    df = pd.DataFrame(data, columns=["problem_id", "result"])
                    df.to_csv("./cache/雨课堂测试-id-{}.csv".format(exam_id), index=False, encoding='utf-8-sig')

                except json.JSONDecodeError:
                    print(f"Response Content: {content[:500]}...")  # 限制长度避免输出过多
            except UnicodeDecodeError:
                print(f"Response Content (raw): {flow.response.content[:500]}...")

