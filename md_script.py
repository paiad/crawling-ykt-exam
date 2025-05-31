from mitmproxy import http
import pandas as pd
import json
from typing import Dict
from tools.utils import remove_html_tags, save_to_file

# 常量定义
TARGET_REQUEST_URL = "examination.xuetangx.com/exam"
TARGET_RESULT_URL_BASE = "https://examination.xuetangx.com/exam_room/problem_results?exam_id="
TARGET_PAPER_URL_BASE = "https://examination.xuetangx.com/exam_room/show_paper?exam_id="


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


def response(flow: http.HTTPFlow) -> None:
    """拦截并处理响应信息"""
    # 从 exam_id.csv 中读取 exam_id
    exam_id = pd.read_csv('exam_id.csv')['exam_id'].iloc[0]
    url = flow.request.pretty_url

    # 处理答题结果并保存 CSV
    if TARGET_RESULT_URL_BASE + str(exam_id) in url:
        handle_result_response(flow, exam_id)

    # 处理试卷内容并输出 Markdown
    elif TARGET_PAPER_URL_BASE + str(exam_id) in url:
        handle_paper_response(flow, exam_id)


def handle_result_response(flow: http.HTTPFlow, exam_id: str) -> None:
    """处理 problem_results 接口的响应，保存 CSV"""
    if not flow.response.content:
        return

    try:
        content = flow.response.content.decode('utf-8')
        json_data = json.loads(content)
        print("====================================================")
        print(json.dumps(json_data, indent=2, ensure_ascii=False))

        problems = json_data["data"]["problem_results"]
        data = []

        for problem in problems:
            item = {
                "problem_id": problem["problem_id"],
                "result": problem["result"]
            }
            if problem.get("answer") is not None:
                item["answer"] = problem["answer"]
            data.append(item)

        df = pd.DataFrame(data, columns=["problem_id", "result", "answer"])
        csv_filename = f"./res/雨课堂测试-id-{exam_id}.csv"
        df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
        print(f"数据已保存到 {csv_filename}")

    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        print(f"Error decoding response: {e}")
        print(f"Raw content: {flow.response.content[:500]}...")


def handle_paper_response(flow: http.HTTPFlow, exam_id: str) -> None:
    """处理 show_paper 接口的响应，保存 Markdown"""
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
                               f"{index}. {body}\n"
                               f"{options}\n\n")

        result_content = result_content.replace("&nbsp;", "")
        cleaned = remove_html_tags(result_content)
        save_to_file(cleaned, f"./md/雨课堂测试-id-{exam_id}.md")
        print("Markdown 文件已保存。")

        print("====================================================")
        print(json.dumps(json_data, indent=2, ensure_ascii=False))

    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        print(f"Error processing paper response: {str(e)}")
        print(f"Raw content: {flow.response.content[:500]}...")


def process_options(problem: Dict, problem_id: str, df: pd.DataFrame) -> tuple[str, str]:
    """根据题目类型处理选项"""
    options = ""
    problem_type = ""
    letters = "ABCDEFGHIJKLMN"

    if problem["Type"] == "SingleChoice":
        options, problem_type = process_single_choice(problem, problem_id, df, letters)
    elif problem["Type"] == "MultipleChoice":
        options, problem_type = process_multiple_choice(problem, problem_id, df, letters)
    elif problem["Type"] in ["FillBlank", "Judgement"]:
        answer = df[df['problem_id'] == problem_id]['answer'].iloc[0]
        options = f"```\n::: details 点我查看答案 & 解析\n{answer}\n:::"
        problem_type = "填空题" if problem["Type"] == "FillBlank" else "判断题"
    else:
        options = "题目类型属于主观题，超出识别范围，请回到原卷识别该题！" + "\n```\n" + "::: details 点我查看答案 & 解析\n:::"
        problem_type = "主观题"

    return options, problem_type


def process_single_choice(problem: Dict, problem_id: str, df: pd.DataFrame, letters: str) -> tuple[str, str]:
    """处理单选题"""
    options = ""
    for i, ele in enumerate(problem["Options"]):
        options += f"{letters[i]}. {ele['value']}\n"
    answer = df[df['problem_id'] == problem_id]['answer'].iloc[0]
    right_pos = next(i for i, opt in enumerate(problem["Options"]) if opt["key"] in answer)
    options += f"```\n::: details 点我查看答案 & 解析\n['{letters[right_pos]}']\n:::"
    return options, "单选题"


def process_multiple_choice(problem: Dict, problem_id: str, df: pd.DataFrame, letters: str) -> tuple[str, str]:
    """处理多选题"""
    options = ""
    right_positions = []
    for i, ele in enumerate(problem["Options"]):
        options += f"{letters[i]}. {ele['value']}\n"
        if ele["key"] in df[df['problem_id'] == problem_id]['answer'].iloc[0]:
            right_positions.append(letters[i])
    options += f"```\n::: details 点我查看答案 & 解析\n{right_positions}\n:::"
    return options, "多选题"
