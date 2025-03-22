from mitmproxy import http
import pandas as pd
import json
from typing import Dict, List
from tools.utils import remove_html_tags, save_to_file

# 常量定义
TARGET_REQUEST_URL = "examination.xuetangx.com/exam"
TARGET_RESPONSE_URL_BASE = "https://examination.xuetangx.com/exam_room/show_paper?exam_id="


def request(flow: http.HTTPFlow) -> None:
    """拦截并打印请求信息"""
    if TARGET_REQUEST_URL not in flow.request.pretty_url:
        return

    print("\n=== New Request ===")
    print(f"URL: {flow.request.pretty_url}")
    print(f"Method: {flow.request.method}")
    print(f"Headers: {dict(flow.request.headers)}")

    if flow.request.content:
        try:
            content = flow.request.content.decode('utf-8')
            print(f"Request Content: {content}")
        except UnicodeDecodeError:
            print(f"Request Content (raw): {flow.request.content}")


def process_options(problem: Dict, problem_id: str, df: pd.DataFrame) -> tuple[str, str]:
    """处理不同类型题目选项"""
    options = ""
    problem_type = ""
    letters = "ABCDEFGHIJKLMN"

    if problem["Type"] == "SingleChoice":
        options, problem_type = process_single_choice(problem, problem_id, df, letters)
    elif problem["Type"] == "MultipleChoice":
        options, problem_type = process_multiple_choice(problem, problem_id, df, letters)
    elif problem["Type"] in ["FillBlank", "Judgement"]:
        options = f"```\n::: details 点我查看答案 & 解析\n{df[df['problem_id'] == problem_id]['answer'].iloc[0]}\n:::"
        problem_type = "填空题" if problem["Type"] == "FillBlank" else "判断题"
    else:
        options = "题目类型属于主观题，超出识别范围，请回到原卷识别该题！"
        problem_type = "主观题"

    return options, problem_type


def process_single_choice(problem: Dict, problem_id: str, df: pd.DataFrame, letters: str) -> tuple[str, str]:
    """处理单选题"""
    options = ""
    for i, ele in enumerate(problem["Options"]):
        options += f"{letters[i]}. {ele['value']}\n"
    result = df[df['problem_id'] == problem_id]['result'].iloc[0]
    answer = df[df['problem_id'] == problem_id]['answer'].iloc[0]
    right_pos = next(i for i, opt in enumerate(problem["Options"]) if opt["key"] in answer)
    options += f"```\n::: details 点我查看答案 & 解析\n{letters[right_pos]}\n:::"
    return options, "单选题"


def process_multiple_choice(problem: Dict, problem_id: str, df: pd.DataFrame, letters: str) -> tuple[str, str]:
    """处理多选题"""
    options = ""
    right_positions = []
    for i, ele in enumerate(problem["Options"]):
        options += f"{letters[i]}. {ele['value']}\n"
        if ele["key"] in df[df['problem_id'] == problem_id]['answer'].iloc[0]:
            right_positions.append(letters[i])
    options += f"\n正确答案为：{right_positions}"
    return options, "多选题"


def response(flow: http.HTTPFlow) -> None:
    """拦截并处理响应信息"""
    exam_id = pd.read_csv('exam_id.csv')['exam_id'].iloc[0]
    target_url = f"{TARGET_RESPONSE_URL_BASE}{exam_id}"

    if target_url not in flow.request.pretty_url:
        return

    if not flow.response.content:
        return

    try:
        content = flow.response.content.decode('utf-8')
        json_data = json.loads(content)
        problems = json_data["data"]["problems"]

        df = pd.read_csv(f"./res/雨课堂测试-id-{exam_id}.csv")
        result_content = ""

        for index, problem in enumerate(problems, 1):
            body = problem["Body"].replace("\n", "").replace(" ", "").strip()
            problem_id = problem["problem_id"]

            options, problem_type = process_options(problem, problem_id, df)
            result_content += (f"```html\n"
                               f"{index}.{body}\n"
                               f"{options}\n\n")

        cleaned_content = remove_html_tags(result_content)
        save_to_file(cleaned_content, f"./txt/雨课堂测试-id-{exam_id}.txt")

        print("====================================================")
        print(json.dumps(json_data, indent=2, ensure_ascii=False))

    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        print(f"Error processing response: {str(e)}")
        print(f"Response Content (raw): {flow.response.content[:500]}...")
