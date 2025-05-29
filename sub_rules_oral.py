from common_message_generator import generate_common_drug_message

def oral_drug_checker(rule_state, rx, messages, error_type, error_rule):
    # BRYPE中 PHER = 急診, 首日量 & stat = 住院, OPD = 門診
    rule = "ORAL-1"
    if rule_state.get(rule) == 'True':
        for bag in rx.get("Data", {}).get("eff_order", []):
            if bag.get("BRYPE", "") == "OPD":
                for order in bag.get("order", []):
                    if int(order.get('DAYS', 0)) == 1 and "內用" in order.get("TYPE", "") and order.get("CODE", "") != "OMIF":
                        messages.append(
                            f"{generate_common_drug_message(order)}，"
                            f"處方開立天數錯誤，藥品總量錯誤，電聯醫師修改處方天數與藥品數量。"
                        )
                        error_type.append("F數量錯誤")
                        error_rule.append(rule)
    return messages, error_type, error_rule