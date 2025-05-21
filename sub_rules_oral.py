def oral_drug_checker(rule_state, rx, messages, error_type, error_rule):
    rule = "ORAL-1"
    if rule_state.get(rule) == 'true':
        for bag in rx.get("Data", {}).get("eff_order", []):
            for order in bag.get("order", []):
                if int(order.get('DAYS', 0)) == 1 and "內用" in order.get("TYPE", ""):
                    messages.append(
                        f"{order.get('DIANAME') or order.get('NAME')}，頻次：{order.get('FREQ', '')}，"
                        f"每次{float(order.get('SD', 0))}粒，總量：{order.get('TXN_QTY', '')}粒，天數 {int(order.get('DAYS', 0))} 天。"
                        f"處方開立天數錯誤，藥品總量錯誤，電聯醫師修改處方天數與藥品數量。"
                    )
                    error_type.append("F數量錯誤")
                    error_rule.append(rule)
    return messages, error_type, error_rule