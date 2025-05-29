from common_message_generator import generate_common_drug_message

def omif_checker(rule_state, rx, messages, error_type, error_rule):
    """
        藥品Lorapseudo SR 120mg/5mg(藥品碼OMIF)規定：
            1. 自費
                --> 總量最多60粒，天數最多30日
            2. 健保
                --> 1天最多2粒。

    """
    rule = 'Other-1'
    if rule_state.get(rule) == 'True':
        for bag in rx.get("Data", {}).get("eff_order", []):
            for order in bag.get("order", []):
                if order.get("CODE", "") == "OMIF":
                    if float(order.get("TXN_QTY", 0))/float(order.get("DAYS", 0)) > 2:
                        messages.append(f"{generate_common_drug_message(order)}，"
                                        f"依據相關規定，{order.get('NAME')} 為自費時每日服用劑量超過上限 (每日最多 2 顆)，"
                                        f"電聯醫師修改。")
                        error_type.append("C劑量錯誤")
                        error_rule.append(rule)
                    if int(order.get("DAYS", 0)) > 30:
                        messages.append(f"{generate_common_drug_message(order)}，"
                                        f"依據相關規定，{order.get('NAME')} 為自費時給藥天數超過 30 日限制，"
                                        f"電聯醫師修改。")
                        error_type.append("F數量錯誤")
                        error_rule.append(rule)

    return messages, error_type, error_rule