import requests
import json

def get_rule_state():
    with open("rule_url.txt", "r", encoding="utf-8") as f:
        url = f.read().strip()  # 去掉換行符號
    payload = {}

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)

    response_data = response.json()
    index_state_map = {
        item.get("index"): item.get("state")
        for item in response_data.get("Data", [])
    }

    return index_state_map

if __name__=='__main__':
    print(get_rule_state())