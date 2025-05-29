import requests
import json

# 設定要傳送的 API URL
# url = "https://www.kutech.tw:3000/medgpt"
url = "http://127.0.0.1:5000/medgpt"

with open(r"order_懷孕.txt", "r", encoding="utf-8") as f:
    payload = json.load(f)

# 設定請求標頭
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)

# 檢查回傳結果
if response.status_code == 200:
    # 解析回傳的 JSON 資料
    response_data = response.json()
    print("回傳資料：\n" + json.dumps(response_data, indent=4, ensure_ascii=False))
    # print("response：\n" + response_data.get("response", "").replace("\\n", "\n"))

else:
    print("API 請求失敗，狀態碼：", response.status_code)
