import os
import json
import requests
import tkinter as tk
from tkinter import filedialog

# 自動將 \ 轉為 /
def normalize_path(path):
    return path.replace("\\", "/")

# 讀取 payload txt
def read_payload_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# 發送請求
def send_request(payload, url):
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"API 失敗，狀態碼：{response.status_code}"}

# 主程式
def main():
    # 選資料夾
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="選擇存有 payload 的資料夾")
    if not folder:
        print("❌ 沒有選擇資料夾")
        return
    folder = normalize_path(folder)

    # 讀取 URL 從 config
    with open("Test_config.json", "r", encoding="utf-8") as f:
        raw_text = f.read().replace("\\", "/")
        config = json.loads(raw_text)
    url = config.get("url")
    if not url:
        print("❌ Test_config.json 中缺少 'url'")
        return

    # 收集結果
    all_results = {}
    txt_files = [f for f in os.listdir(folder) if f.lower().endswith(".txt")]

    for filename in txt_files:
        file_path = os.path.join(folder, filename)
        try:
            payload = read_payload_file(file_path)
            result = send_request(payload, url)

            # 印出結果
            print(f"\n📄 檔案：{filename}")
            print(json.dumps(result, ensure_ascii=False, indent=4))

            all_results[filename] = result
        except Exception as e:
            print(f"\n⚠️ 錯誤：{filename} → {e}")
            all_results[filename] = {"error": str(e)}

    # 寫入結果檔
    output_path = os.path.join(folder, "Batch_API_results.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=4)

    print(f"\n✅ 所有結果已儲存至：{output_path}")

if __name__ == "__main__":
    main()
