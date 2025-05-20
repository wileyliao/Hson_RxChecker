def insured_cannot_selfpay(order, bag, messages, error_type, error_rule):
    rule = "ADC-1"
    rule_describe = "具健保身分的病人，不得自費開立管制藥品"

    if bag.get("PATNAME")=="False" and order.get("CTYPE", "") == "自費":
        messages.append(
            f"{order.get('DIANAME') or order.get('NAME')}，頻次：{order.get('FREQ', '')}，"
            f"每次{float(order.get('SD', 0))}粒，總量：{order.get('TXN_QTY', '')}粒，天數 {int(order.get('DAYS', 0))} 天。"
            f"依據相關規定，具健保身分的病人，不得自費開立管制藥品，"
            f"電聯醫師修改。")
        error_type.append("I其他")
        error_rule.append(rule)

    return messages, error_type, error_rule


def foreign_control_drug_limit(order, bag, messages, error_type, error_rule):
    rule = "ADC-2"
    rule_describe = "無健保身分，開立管制藥品種類數規定"

    if bag.get("PATNAME") == "False":

        control_drug_count = len(bag.get("order", []))
        max_control_types = 2 if bag.get("SECTNO") == "精神科" else 1

        if control_drug_count > max_control_types and not bag.get("_warned_control_type_limit", False):
            # 整合所有藥品詳情成文字串
            detail_lines = []
            for each_order in bag.get("order", []):
                detail = (
                    f"{each_order.get('DIANAME') or each_order.get('NAME')}，頻次：{each_order.get('FREQ', '')}，"
                    f"每次{float(each_order.get('SD', 0))}粒，總量：{each_order.get('TXN_QTY', '')}粒，天數 {int(each_order.get('DAYS', 0))} 天"
                )
                detail_lines.append(detail)

            full_message = (
                f"此處方開立了 {control_drug_count} 種管制藥品：\n" +
                "；\n".join(detail_lines) + "。\n" +
                f"依據相關規定，無健保身分在{bag.get('SECTNO')}最多開立 {max_control_types} 種管制藥品。"
                f"電聯醫師修改"
            )

            messages.append(full_message)
            error_type.append("I其他")
            error_rule.append(rule)
            bag["_warned_control_type_limit"] = True

    return messages, error_type, error_rule


def foreign_max_days(order, bag, messages, error_type, error_rule):
    rule = "ADC-3"
    rule_describe = "無健保身分，開立管制藥品天數規定"

    if bag.get("PATNAME") == "True":
        max_days = 30 if bag.get("SECTNO") == "精神科" else 7
        if int(order.get("DAYS", 0)) > max_days:
            messages.append(
                f"{order.get('DIANAME') or order.get('NAME')}，頻次：{order.get('FREQ', '')}，"
                f"每次{float(order.get('SD', 0))}粒，總量：{order.get('TXN_QTY', '')}粒，天數 {int(order.get('DAYS', 0))} 天。"
                f"依據相關規定，{bag.get('SECTNO')}自費開立之管制藥品，給藥最大天數為 {max_days} 天，"
                f"電聯醫師修改。")
            error_type.append("F數量錯誤")
            error_rule.append(rule)

    return messages, error_type, error_rule


def foreign_max_dosage(order, bag, messages, error_type, error_rule):
    rule = "ADC-4"
    rule_describe = "無健保身分，開立管制藥品劑量規定"

    if bag.get("PATNAME") == "True":
        if float(order.get("SD", 0)) > 1:
            messages.append(
                f"{order.get('DIANAME') or order.get('NAME')}，頻次：{order.get('FREQ', '')}，"
                f"每次{float(order.get('SD', 0))}粒，總量：{order.get('TXN_QTY', '')}粒，天數 {int(order.get('DAYS', 0))} 天。"
                f"依據相關規定，無健保身分的病人，自費管制藥品劑量限量 1 粒，"
                f"電聯醫師修改。")
            error_type.append("C劑量錯誤")
            error_rule.append(rule)

    return messages, error_type, error_rule


def doctor_cannot_prescribe_self(order, bag, messages, error_type, error_rule):
    rule = "ADC-5"
    rule_describe = "醫師不得為本人開立管制藥品"

    if bag.get("DOC") == "True":
        messages.append(
            f"{order.get('DIANAME') or order.get('NAME')}，頻次：{order.get('FREQ', '')}，"
            f"每次{float(order.get('SD', 0))}粒，總量：{order.get('TXN_QTY', '')}粒，天數 {int(order.get('DAYS', 0))} 天。"
            f"依據相關規定，醫師不得為本人開立管制藥品，"
            f"電聯醫師修改。")
        error_type.append("I其他")
        error_rule.append(rule)

    return messages, error_type, error_rule


def oral_drug_checker(order, messages, error_type, error_rule):
    rule = "ORAL-1"
    rule_describe = "口服藥品不能只開立一天"

    if int(order.get('DAYS', 0)) == 1 and "內用" in order.get("TYPE", ""):
        messages.append(
            f"{order.get('DIANAME') or order.get('NAME')}，頻次：{order.get('FREQ', '')}，"
            f"每次{float(order.get('SD', 0))}粒，總量：{order.get('TXN_QTY', '')}粒，天數 {int(order.get('DAYS', 0))} 天。"
            f"處方開立天數錯誤，藥品總量錯誤，電聯醫師修改處方天數與藥品數量。"
        )
        error_type.append("F數量錯誤")
        error_rule.append(rule)
    return messages, error_type, error_rule