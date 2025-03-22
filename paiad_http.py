import requests
import pandas as pd

from tools.private_key import TOKEN

# 请求部分
url = "https://examination.xuetangx.com/exam_room/cache_results?exam_id=3043182"
headers = {
    "cookie": "x_access_token={};".format(TOKEN)
}

try:
    # 发送请求并直接解析 JSON
    response = requests.get(url, headers=headers, timeout=10)
    print("状态码:", response.status_code)

    # 转换为 DataFrame
    df = pd.DataFrame(response.json()["data"]["results"])

    # 保存为 CSV
    df[["problem_id", "result"]].to_csv("./cache/other.csv", index=False)

    print("数据已保存到 exam_results.csv")

except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
except Exception as e:
    print(f"处理失败: {e}")