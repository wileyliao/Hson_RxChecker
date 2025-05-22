def diabetes_checker(rule_state, rx, messages, error_type, error_rule):
    rule = "CLIN-1"
    diabetes_icd_code = ["E08", "E09", "E10", "E11", "E12", "E13", "O24"]
    if rule_state.get(rule) == 'True':
        icd = rx.get("Data", {}).get("eff_order", [])[0].get("ICD_CODE").split(';')
        if  not any(code.startswith(prefix) for code in icd for prefix in diabetes_icd_code):
            for bag in rx.get("Data", {}).get("eff_order", []):
                for order in bag.get("order", []):
                    if (order.get('ATC', "")).startswith('A10'):
                        messages.append(
                            f"{order.get('DIANAME') or order.get('NAME')}，頻次：{order.get('FREQ', '')}，"
                            f"每次{float(order.get('SD', 0))} {order.get('DUNIT', '')}，總量：{order.get('TXN_QTY', '')} {order.get('DUNIT', '')}，天數 {int(order.get('DAYS', 0))} 天。"
                            f"非糖尿病診斷，電聯醫師確認處方與診斷，確認是否開立該藥品。"
                        )
                        error_type.append("I適應症錯誤")
                        error_rule.append(rule)
    return messages, error_type, error_rule


def airway_disease_checker(rule_state, rx, messages, error_type, error_rule):
    rule = "CLIN-2"
    diabetes_icd_code = ["J41", "J42", "J43", "J44", "J45"]
    if rule_state.get(rule) == 'True':
        icd = rx.get("Data", {}).get("eff_order", [])[0].get("ICD_CODE").split(';')
        if  any(code.startswith(prefix) for code in icd for prefix in diabetes_icd_code):
            for bag in rx.get("Data", {}).get("eff_order", []):
                for order in bag.get("order", []):
                    if (order.get('ATC', "")).startswith('C07AB'):
                        messages.append(
                            f"{order.get('DIANAME') or order.get('NAME')}，頻次：{order.get('FREQ', '')}，"
                            f"每次{float(order.get('SD', 0))} {order.get('DUNIT', '')}，總量：{order.get('TXN_QTY', '')} {order.get('DUNIT', '')}，天數 {int(order.get('DAYS', 0))} 天。"
                            f"氣喘或是慢性肺阻塞疾病診斷，不建議使用β受體阻斷劑。"
                        )
                        error_type.append("O其他-藥物選用適切性")
                        error_rule.append(rule)
    return messages, error_type, error_rule