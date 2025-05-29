def generate_common_drug_message(order):
    return (f"{order.get('NAME')}，頻次：{order.get('FREQ', '')}，"
            f"每次{float(order.get('SD', 0))} {order.get('DUNIT', '')}，"
            f"總量：{order.get('TXN_QTY', '')} {order.get('DUNIT', '')}，"
            f"天數 {int(order.get('DAYS', 0))} 天")