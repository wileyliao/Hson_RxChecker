import json
import time
from flask import Flask, request, jsonify
from rx_checker_main import main
from rule_get import get_rule_state
import os
from datetime import datetime
# === 取得今天日期 ===


app = Flask(__name__)

@app.route('/medgpt', methods=['POST'])
def rx_checker():
    today_str = datetime.now().strftime("%Y%m%d")
    log_dir = "log"
    log_file_path = os.path.join(log_dir, f"{today_str}.txt")
    os.makedirs(log_dir, exist_ok=True)

    try:
        total_start = time.time()

        rx = request.get_json()

        rule_state_start = time.time()
        try:
            rule_state = get_rule_state()
        except Exception as e:
            return jsonify({"error": f"❌ 無法取得規則狀態：{str(e)}"}), 500
        rule_state_duration = round(time.time() - rule_state_start, 3)

        # 產生邏輯，尚未含 API總耗時
        messages, error_types, error_rules, log_data = main(
            rx, rule_state, rule_state_duration
        )

        # 補上 API總耗時
        api_response_duration = round(time.time() - total_start, 3)
        log_data["API總耗時s"] = api_response_duration

        # 寫入 log 檔
        with open(log_file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_data, ensure_ascii=False) + "\n")


        local_prompt = None
        if messages:
            local_prompt = "\n".join([f"{i+1}. {msg}" for i, msg in enumerate(list(set(messages)))])

        result_dict = {
            "MED_BAG_SN": rx["Data"]["eff_order"][0]["MED_BAG_SN"],
            "error": str(bool(messages)),
            "error_type": list(set(error_types)),
            "rule_type": list(set(error_rules)),
            "response": local_prompt
        }

        return jsonify(result_dict), 200

    except Exception as e:
        return jsonify({"error": f"❌ 伺服器內部錯誤：{str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
