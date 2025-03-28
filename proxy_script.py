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
    target_url = "https://examination.xuetangx.com/exam_room/show_paper?exam_id="
    exam_id = pd.read_csv('exam_id.csv')['exam_id'].iloc[0]
    target_url += str(exam_id)

    if flow.request.pretty_url == target_url:

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

                    problems = json_data["data"]["problems"]
                    # print(problems)
                    res = ""
                    index = 0
                    for problem in problems:
                        count = 0
                        Options = ""
                        body = problem["Body"]
                        type = problem["Type"]
                        problem_id = problem["problem_id"]
                        if "Answer" in problem:
                            answer = str(problem["Answer"])
                        else:
                            answer = ""
                        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"]
                        if type == "SingleChoice":
                            """
                            [{'key': 'C', 'value': 'ROM'},
                            {'key': 'B', 'value': 'Hard disks'},
                            {'key': 'A', 'value': 'RAM'},
                            {'key': 'D', 'value': 'Solid-state storage'}]
                            """
                            for ele in problem["Options"]:
                                Options += letters[count] + ". " + ele["value"] + "\n"
                                count += 1
                            Options += "\n单选题的答案为："
                            problem_type = "单选题"
                        elif type == "MultipleChoice":
                            for ele in problem["Options"]:
                                Options += letters[count] + ". " + ele["value"] + "\n"
                                count += 1
                            Options += "\n多选题的答案为："
                            problem_type = "多选题"
                        elif type == "FillBlank":
                            Options = "填空题的答案为："
                            problem_type = "填空题"
                        elif type == "Judgement":
                            Options = "判断题的答案为："
                            problem_type = "判断题"
                        else:
                            Options = "题目类型属于主观题，超出识别范围，请回到原卷识别该题！"
                            problem_type = "主观题"
                        index += 1
                        body_new = str(body).replace("\n", "").replace("&nbsp", "").strip(" ")
                        Options_new = str(Options).replace("&nbsp", "").strip(" ")
                        res += ("===第{}题 题型为：{}===ProblemId：{}==\n".format(index, problem_type, problem_id)
                                + body_new + "\n"
                                + Options_new + answer
                                + "\n\n=========================\n\n\n")
                        res = remove_html_tags(res)
                    save_to_file(f"爬取地址URL：\n{flow.request.pretty_url}\n内容: \n{res}",
                                 filename="./txt/雨课堂测试-id-{}.txt".format(exam_id))
                except json.JSONDecodeError:
                    print(f"Response Content: {content[:500]}...")  # 限制长度避免输出过多
            except UnicodeDecodeError:
                print(f"Response Content (raw): {flow.response.content[:500]}...")
