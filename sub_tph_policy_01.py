# tph_policy.py

def tph_policy_01(order, bag, messages, error_type):
    """
        管制藥品開立規定
            1. 具健保身分的病人(這裡以'病人姓名不為外國名字'來判斷)
                --> 不得自費開立管制藥品
            2. 不具健保身分的病人(這裡以'病人姓名為外國名字')
                2.1. 給藥種類限制
                    --> 精神科最多兩種為限
                    --> 其他科最多一種為限
                2.2. 給藥天數限制
                    --> 精神科最多30日為限
                    --> 其他科最多7日為限
                2.3. 給藥劑量限制
                    --> 不分科別，至多一粒為限
            3. 醫師不得為自己開立管制藥品
    """
    max_days = 30 if bag.get("SECTNO") == "精神科" else 7
    is_foreign_patient = bag.get("PATNAME") == "True"

    # Step 1: 藥品類型過濾
    if order.get("TYPE") in ["注射藥", "點滴"]:
        return messages, error_type

    # Step 2: 非管制藥過濾
    if order.get("DRUGKIND") == "N":
        return messages, error_type

    # ====== 即時統計控制藥品數量，並判斷是否超過 ======
    control_drug_count = 0
    for each_order in bag.get("order", []):
        if each_order.get("TYPE") in ["注射藥", "點滴"]:
            continue
        if each_order.get("DRUGKIND") == "N":
            continue
        if each_order.get("CODE") == "OMIF":
            continue
        control_drug_count += 1

    max_control_types = 2 if bag.get("SECTNO") == "精神科" else 1
    if control_drug_count > max_control_types:
        if not bag.get("_warned_control_type_limit", False):
            messages.append(f"此處方開立了 {control_drug_count} 種管制藥品，依據相關規定{bag.get('SECTNO')}最多開立 {max_control_types} 種。")
            error_type.append("I其他")
            bag["_warned_control_type_limit"] = True
    # ==================================================

    # Step 3: 病人國籍判斷
    if is_foreign_patient:
        if order.get("CTYPE", "") != "自費":
            return messages, error_type

        if int(order.get("DAYS", 0)) > max_days:
            messages.append(f"{order.get('DIANAME') or order.get('NAME')}，頻次：{order.get('FREQ', '')}，"
                            f"每次{float(order.get('SD', 0))}粒，總量：{order.get('TXN_QTY', '')}粒，天數 {int(order.get('DAYS', 0))} 天。"
                            f"依據相關規定，{bag.get('SECTNO')}自費開立之管制藥品，給藥最大天數為 {max_days} 天，"
                            f"電聯醫師修改。")
            error_type.append("F數量錯誤")

        if float(order.get("SD", 0)) > 1:
            messages.append(f"{order.get('DIANAME') or order.get('NAME')}，頻次：{order.get('FREQ', '')}，"
                            f"每次{float(order.get('SD', 0))}粒，總量：{order.get('TXN_QTY', '')}粒，天數 {int(order.get('DAYS', 0))} 天。"
                            f"依據相關規定，無健保身分的病人，自費管制藥品劑量限量 1 粒，"
                            f"電聯醫師修改。")
            error_type.append("C劑量錯誤")

    else:
        if order.get("CTYPE", "") == "自費":
            messages.append(f"{order.get('DIANAME') or order.get('NAME')}，頻次：{order.get('FREQ', '')}，"
                            f"每次{float(order.get('SD', 0))}粒，總量：{order.get('TXN_QTY', '')}粒，天數 {int(order.get('DAYS', 0))} 天。"
                            f"依據相關規定，具健保身分的病人，不得自費開立管制藥品，"
                            f"電聯醫師修改。")
            error_type.append("I其他")

    # 醫師自我開藥
    if bag.get("DOC") == "True":
        messages.append(f"{order.get('DIANAME') or order.get('NAME')}，頻次：{order.get('FREQ', '')}，"
                        f"每次{float(order.get('SD', 0))}粒，總量：{order.get('TXN_QTY', '')}粒，天數 {int(order.get('DAYS', 0))} 天。"
                        f"依據相關規定，醫師不得為本人開立管制藥品，"
                        f"電聯醫師修改。")
        error_type.append("I其他")

    return messages, error_type
