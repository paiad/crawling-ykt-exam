# @Software  :PyCharm
# @Author    : paiad
# @File      : commit.py
# @Time      : 2025-03-22 16:41
from mitmproxy import http
import pandas as pd
import json

from tools.utils import remove_html_tags, save_to_file


def response(flow: http.HTTPFlow) -> None:
    """
    在响应返回给客户端前，拦截并打印响应信息
    """
    target_url = "https://examination.xuetangx.com/exam_room/show_paper?exam_id="
    exam_id = pd.read_csv('exam_id.csv')['exam_id'].iloc[0]
    target_url += str(exam_id)

    if flow.request.pretty_url == target_url:
        if flow.response.content:
            try:
                content = flow.response.content.decode('utf-8')
                try:
                    json_data = json.loads(content)
                    pretty_json = json.dumps(json_data, indent=2, ensure_ascii=False)
                    print("====================================================")
                    print(pretty_json)

                    problems = json_data["data"]["problems"]
                    res = ""
                    index = 0
                    for problem in problems:
                        count = 0
                        Options = ""
                        body = problem["Body"]
                        type = problem["Type"]
                        problem_id = problem["problem_id"]
                        answer = str(problem.get("Answer", ""))  # Use get() with default empty string
                        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "ERROR"]
                        df = pd.read_csv("cache/personal.csv")
                        df_diff = pd.read_csv("./contrast/diff_problem_ids.csv")
                        problem_ids = df_diff["problem_id"].tolist()

                        if type == "SingleChoice":
                            print("&&&&&&&&&&&&&&&&&&&&&&&")
                            label = -1
                            for ele in problem["Options"]:
                                key_res = df[df['problem_id'] == problem_id]['result'].iloc[0]
                                print("=============\n" + ele['key'] + key_res + "\n======")
                                if ele['key'] in key_res:
                                    label = count
                                Options += letters[count] + ". " + ele["value"] + "\n"
                                count += 1
                            Options += "\n我的单选题的答案为：\n" + letters[label]
                            problem_type = "单选题"
                        elif type == "MultipleChoice":
                            label_multi = []  # Initialize here before the loop
                            for ele in problem["Options"]:
                                key_res = df[df['problem_id'] == problem_id]['result'].iloc[0]
                                if ele['key'] in key_res:
                                    label_multi.append(count)
                                Options += letters[count] + ". " + ele["value"] + "\n"
                                count += 1
                            Options += "\n多选题的答案为：" + str([letters[x] for x in label_multi])
                            problem_type = "多选题"
                        elif type == "FillBlank":
                            Options = "\n填空题的答案为：\n" + str(df[df['problem_id'] == problem_id]['result'].iloc[0])
                            problem_type = "填空题"
                        elif type == "Judgement":
                            Options = "\n判断题的答案为：" + str(df[df['problem_id'] == problem_id]['result'].iloc[0])
                            problem_type = "判断题"
                        else:
                            Options = "题目类型属于主观题，超出识别范围，请回到原卷识别该题！"
                            problem_type = "主观题"

                        index += 1
                        body_new = str(body).replace("\n", "").replace(" ", "").strip(" ")
                        Options_new = str(Options).replace(" ", "").strip(" ")

                        spec = "===第{}题 题型为：{}===\n".format(index,
                                                                 problem_type) + body_new + "\n" + Options_new + answer + "\n\n=========================\n\n\n"

                        if problem_id in problem_ids:
                            spec = "```html\n" + "???" + spec + "\n```\n"

                        res = res + spec
                        res = remove_html_tags(res)
                    save_to_file(f"爬取地址URL：\n{flow.request.pretty_url}\n内容: \n{res}",
                                 filename="./md/cache-雨课堂测试-id-{}.md".format(exam_id))
                except json.JSONDecodeError:
                    print(f"Response Content: {content[:500]}...")  # 限制长度避免输出过多
            except UnicodeDecodeError:
                print(f"Response Content (raw): {flow.response.content[:500]}...")
