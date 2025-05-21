# rx_checker_app.py

# import pandas as pd
# from dotenv import load_dotenv
# import os
# from openai import OpenAI
import json
from flask import Flask, request, jsonify
from rx_checker_main import main
from rule_get import get_rule_state

app = Flask(__name__)

global_prompt = (f"你是一名藥師助理，負責審查處方有沒有符合'規定'。\n"
                 f"請用正式且簡短明確的語氣，先指出下列你所發現的問題，不需稱呼或問候。")
traditional_prompt = f"\n請以繁體中文回覆。"

EXCEPTION_DRUGS = []

@app.route('/medgpt', methods=['POST'])
def rx_checker():
    rx = request.get_json()
    rule_state = get_rule_state()

    local_prompt = None

    messages, error_types, error_rules = main(rx, rule_state)

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
