import requests
import json

# 讀取配置檔案，並自動將反斜線 \ 轉為正斜線 /
def read_config():
    with open("Test_config.json", "r", encoding="utf-8") as f:
        raw_text = f.read()
    raw_text = raw_text.replace("\\", "/")
    return json.loads(raw_text)

# 讀取配置檔案中的 url 和 order_file
config = read_config()
url = config.get("url")
order_file = config.get("order_file")

if not url:
    raise ValueError("❌ Test_config.json 中缺少 'url'")
if not order_file:
    raise ValueError("❌ Test_config.json 中缺少 'order_file'")

# 從指定的 txt 檔案讀取 payload
with open(order_file, "r", encoding="utf-8") as f:
    payload = json.load(f)

# 設定請求標頭
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)

# 檢查回傳結果
if response.status_code == 200:
    response_data = response.json()
    print("回傳資料：\n" + json.dumps(response_data, indent=4, ensure_ascii=False))
else:
    print("API 請求失敗，狀態碼：", response.status_code)
    try:
        print("伺服器回應：", response.json())
    except Exception as e:
        print("⚠️ 回應不是 JSON 格式，內容如下：")
        print(response.text)

