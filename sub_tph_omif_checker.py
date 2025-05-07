def omif_checker(order, messages, error_type):
    """
        藥品Lorapseudo SR 120mg/5mg(藥品碼OMIF)規定：
            1. 自費
                --> 總量最多60粒，天數最多30日
            2. 健保
                --> 1天最多2粒。

    """
    sd = float(order.get("SD", 0))
    days = int(order.get("DAYS", 0))
    qty = int(order.get("TXN_QTY", 0))
    ctype = order.get("CTYPE", "")


    freq_times = (qty/days)/sd
    daily_dose = sd * freq_times

    if ctype == "自費":
        if daily_dose > 2:
            messages.append(f"{order.get('DIANAME') or order.get('NAME')}，頻次：{order.get('FREQ', '')}，"
                            f"每次{order.get('SD', '')}粒，總量：{order.get('TXN_QTY', '')}粒，天數 {int(order.get('DAYS', 0))} 天。"
                            f"依據相關規定，{order.get('DIANAME') or order.get('NAME')} 為自費時每日服用劑量超過上限 (每日最多 2 顆)，"
                            f"電聯醫師修改。")
            error_type.append("C劑量錯誤")
        if days > 30:
            messages.append(f"{order.get('DIANAME') or order.get('NAME')}，頻次：{order.get('FREQ', '')}，"
                            f"每次{order.get('SD', '')}粒，總量：{order.get('TXN_QTY', '')}粒，天數 {int(order.get('DAYS', 0))} 天。"
                            f"依據相關規定，{order.get('DIANAME') or order.get('NAME')} 為自費時給藥天數超過 30 日限制，"
                            f"電聯醫師修改。")
            error_type.append("F數量錯誤")
        if qty > 60:
            messages.append(f"{order.get('DIANAME') or order.get('NAME')}，頻次：{order.get('FREQ', '')}，"
                            f"每次{order.get('SD', '')}粒，總量：{order.get('TXN_QTY', '')}粒，天數 {int(order.get('DAYS', 0))} 天。"
                            f"依據相關規定，{order.get('DIANAME') or order.get('NAME')} 為自費時總顆數超過 60 粒限制，"
                            f"電聯醫師修改。")
            error_type.append("F數量錯誤")
    elif ctype == "健保":
        if daily_dose > 2:
            messages.append(f"{order.get('DIANAME') or order.get('NAME')}，頻次：{order.get('FREQ', '')}，"
                            f"每次{order.get('SD', '')}粒，總量：{order.get('TXN_QTY', '')}粒，天數 {int(order.get('DAYS', 0))} 天。"
                            f"依據相關規定，{order.get('DIANAME') or order.get('NAME')} 為健保時每日服用劑量超過上限 (每日最多 2 顆)，"
                            f"電聯醫師修改。")
            error_type.append("C劑量錯誤")

    return messages, error_type