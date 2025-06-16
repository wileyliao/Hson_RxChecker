import json

def print_json_pretty(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"❌ 發生錯誤：{e}")

if __name__ == "__main__":
    file_path = "log_output.txt"  # 如果檔名不同可自行修改
    print_json_pretty(file_path)
