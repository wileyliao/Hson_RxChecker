# sub_tph_policy_02.py

def tph_policy_02(order, messages, error_type):
    """
        口服藥品不能只開立一天
    """
    if int(order.get('DAYS', 0)) == 1:
        messages.append(
            f"{order.get('DIANAME') or order.get('NAME')}，頻次：{order.get('FREQ', '')}，"
            f"每次{float(order.get('SD', 0))}粒，總量：{order.get('TXN_QTY', '')}粒，天數 {int(order.get('DAYS', 0))} 天。"
            f"處方開立天數錯誤，藥品總量錯誤，電聯醫師修改處方天數與藥品數量。"
        )
        error_type.append("F數量錯誤")
    return messages, error_type
