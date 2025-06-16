rules_required_fields = {
    "ADC-1": ["CODE", "CTYPE", "DRUGKIND", "PATNAME", "TYPE"],
    "ADC-2": ["CODE", "DRUGKIND", "PATNAME", "SECTNO", "TYPE"],
    "ADC-3": ["CODE", "DAYS", "DRUGKIND", "PATNAME", "SECTNO", "TYPE"],
    "ADC-4": ["CODE", "DRUGKIND", "PATNAME", "SD", "TYPE"],
    "ADC-5": ["CODE", "DOC", "DRUGKIND", "TYPE"],
    "CLIN-1": ["ICD_CODE", "ATC"],
    "CLIN-2": ["ICD_CODE", "ATC"],
    "CLIN-3": ["PREGNANT", "PREGNANCY_LEVEL"],
    "Other-1": ["CODE", "TXN_QTY", "DAYS", "NAME"],
    "ORAL-1": ["BRYPE", "DAYS", "TYPE", "CODE"]
}

def generate_log(rx, triggered_rules: set, rule_state: dict,
                 rule_state_duration: float):
    bag = rx["Data"]["eff_order"][0]
    med_bag_sn = bag.get("MED_BAG_SN", "UNKNOWN")
    bag_orders = bag.get("order", [])

    drug_logs = []

    for order in bag_orders:
        log_entries = []

        for rule, fields in rules_required_fields.items():
            field_values = {}
            has_missing = False

            for field in fields:
                value = order.get(field)
                if value is None:
                    value = bag.get(field)
                if value is None:
                    value = "None"
                    has_missing = True
                field_values[field] = value

            result = "missing_value" if has_missing else (
                "fail" if rule in triggered_rules else "pass"
            )

            log_entries.append({
                "規則": rule,
                "規則狀態": rule_state.get(rule, "UNKNOWN"),
                "所需欄位": field_values,
                "result": result
            })

        drug_logs.append({
            "藥品名稱": order.get("NAME", "UNKNOWN"),
            "log": log_entries
        })

    output_data = {
        "藥袋編號": med_bag_sn,
        "藥品列表": drug_logs,
        "規則狀態取得耗時s": rule_state_duration
        # ⛔ "API總耗時s" 不寫在這裡，由外層補上
    }

    return output_data
