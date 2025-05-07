# rx_checker_app.py

# import pandas as pd
# from dotenv import load_dotenv
# import os
# from openai import OpenAI
import json
from flask import Flask, request, jsonify

from sub_tph_omif_checker import *
from sub_tph_policy_01 import *
from sub_tph_policy_02 import *

app = Flask(__name__)

global_prompt = (f"你是一名藥師助理，負責審查處方有沒有符合'規定'。\n"
                 f"請用正式且簡短明確的語氣，先指出下列你所發現的問題，不需稱呼或問候。")
traditional_prompt = f"\n請以繁體中文回覆。"

EXCEPTION_DRUGS = []

@app.route('/medgpt', methods=['POST'])
def med_gpt_main():
    messages = []
    error_type = []
    local_prompt = None

    json_data = request.get_json()

    for bag in json_data.get("Data", {}).get("eff_order", []):
        for order in bag.get("order", []):
            if order.get("CODE", "") == "OMIF":
                messages, error_type = omif_checker(order, messages, error_type)

            messages, error_type = tph_policy_01(order, bag, messages, error_type)
            messages, error_type = tph_policy_02(order, messages, error_type)

    if messages:
        local_prompt = "\n".join([f"{i+1}. {msg}" for i, msg in enumerate(list(set(messages)))])

    result_dict = {
        "MED_BAG_SN": bag.get("MED_BAG_SN"),
        "error": str(bool(messages)),
        "error_type": list(set(error_type)),
        "response": local_prompt
    }

    return jsonify(result_dict), 200


if __name__ == '__main__':
    app.run(debug=True)
