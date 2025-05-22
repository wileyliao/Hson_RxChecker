def insured_cannot_selfpay(rule_state, rx, messages, error_type, error_rule):
    rule = "ADC-1"
    if rule_state.get(rule) == 'True':

        for bag in rx.get("Data", {}).get("eff_order", []):
            for order in bag.get("order", []):
                if "內用" in order.get("TYPE", "") and order.get("DRUGKIND") != "N" and order.get("CODE", "") != "OMIF":
                    if bag.get("PATNAME") == "False" and order.get("CTYPE", "") == "自費":
                        messages.append(
                            f"{order.get('DIANAME') or order.get('NAME')}，頻次：{order.get('FREQ', '')}，"
                            f"每次{float(order.get('SD', 0))} {order.get('DUNIT', '')}，總量：{order.get('TXN_QTY', '')} {order.get('DUNIT', '')}，天數 {int(order.get('DAYS', 0))} 天。"
                            f"依據相關規定，具健保身分的病人，不得自費開立管制藥品，"
                            f"電聯醫師修改。")
                        error_type.append("O其他")
                        error_rule.append(rule)
    return messages, error_type, error_rule


def foreign_control_drug_limit(rule_state, rx, messages, error_type, error_rule):
    rule = "ADC-2"
    if rule_state.get(rule) == 'True':
        for bag in rx.get("Data", {}).get("eff_order", []):
            if bag.get("PATNAME") == "True":
                non_omif_orders = [order for order in bag.get("order", []) if order.get("CODE", "") != "OMIF"]
                control_drug_count = len(bag.get("order", []))
                max_control_types = 2 if bag.get("SECTNO") == "精神科" else 1

                if control_drug_count > max_control_types and not bag.get("_warned_control_type_limit", False):
                    detail_lines = []
                    for each_order in non_omif_orders:
                        detail_lines.append(
                            f"{each_order.get('DIANAME') or each_order.get('NAME')}，頻次：{each_order.get('FREQ', '')}，"
                            f"每次{float(each_order.get('SD', 0))} {each_order.get('DUNIT', '')}，總量：{each_order.get('TXN_QTY', '')} {each_order.get('DUNIT', '')}，天數 {int(each_order.get('DAYS', 0))} 天"
                        )
                    messages.append(
                        f"此處方開立了 {control_drug_count} 種管制藥品：\n" +
                        "；\n".join(detail_lines) + "。\n" +
                        f"依據相關規定，無健保身分在{bag.get('SECTNO')}最多開立 {max_control_types} 種管制藥品。"
                        f"電聯醫師修改"
                    )
                    error_type.append("O其他")
                    error_rule.append(rule)
                    bag["_warned_control_type_limit"] = True
    return messages, error_type, error_rule


def foreign_max_days(rule_state, rx, messages, error_type, error_rule):
    rule = "ADC-3"
    if rule_state.get(rule) == 'True':
        for bag in rx.get("Data", {}).get("eff_order", []):
            if bag.get("PATNAME") == "True":
                max_days = 30 if bag.get("SECTNO") == "精神科" else 7
                for order in bag.get("order", []):
                    if "內用" in order.get("TYPE", "") and order.get("DRUGKIND") != "N" and order.get("CODE", "") != "OMIF":
                        if int(order.get("DAYS", 0)) > max_days:
                            messages.append(
                                f"{order.get('DIANAME') or order.get('NAME')}，頻次：{order.get('FREQ', '')}，"
                                f"每次{float(order.get('SD', 0))} {order.get('DUNIT', '')}，總量：{order.get('TXN_QTY', '')} {order.get('DUNIT', '')}，天數 {int(order.get('DAYS', 0))} 天。"
                                f"依據相關規定，{bag.get('SECTNO')}自費開立之管制藥品，給藥最大天數為 {max_days} 天，"
                                f"電聯醫師修改。")
                            error_type.append("F數量錯誤")
                            error_rule.append(rule)
    return messages, error_type, error_rule


def foreign_max_dosage(rule_state, rx, messages, error_type, error_rule):
    rule = "ADC-4"
    if rule_state.get(rule) == 'True':
        for bag in rx.get("Data", {}).get("eff_order", []):
            if bag.get("PATNAME") == "True":
                for order in bag.get("order", []):
                    if "內用" in order.get("TYPE", "") and order.get("DRUGKIND") != "N" and order.get("CODE", "") != "OMIF":
                        if float(order.get("SD", 0)) > 1:
                            messages.append(
                                f"{order.get('DIANAME') or order.get('NAME')}，頻次：{order.get('FREQ', '')}，"
                                f"每次{float(order.get('SD', 0))} {order.get('DUNIT', '')}，總量：{order.get('TXN_QTY', '')} {order.get('DUNIT', '')}，天數 {int(order.get('DAYS', 0))} 天。"
                                f"依據相關規定，無健保身分的病人，自費管制藥品劑量限量 1 粒，"
                                f"電聯醫師修改。")
                            error_type.append("C劑量錯誤")
                            error_rule.append(rule)
    return messages, error_type, error_rule


def doctor_cannot_prescribe_self(rule_state, rx, messages, error_type, error_rule):
    rule = "ADC-5"
    if rule_state.get(rule) == 'True':
        for bag in rx.get("Data", {}).get("eff_order", []):
            if bag.get("DOC") == "True":
                for order in bag.get("order", []):
                    if "內用" in order.get("TYPE", "") and order.get("DRUGKIND") != "N" and order.get("CODE", "") != "OMIF":
                        messages.append(
                            f"{order.get('DIANAME') or order.get('NAME')}，頻次：{order.get('FREQ', '')}，"
                            f"每次{float(order.get('SD', 0))} {order.get('DUNIT', '')}，總量：{order.get('TXN_QTY', '')} {order.get('DUNIT', '')}，天數 {int(order.get('DAYS', 0))} 天。"
                            f"依據相關規定，醫師不得為本人開立管制藥品，"
                            f"電聯醫師修改。")
                        error_type.append("O其他")
                        error_rule.append(rule)
    return messages, error_type, error_rule
