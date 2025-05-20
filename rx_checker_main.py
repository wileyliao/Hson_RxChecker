from sub_rules import *
from sub_tph_omif_checker import omif_checker

def main(rx, rule_state):
    error_type = []
    messages = []
    error_rule = []

    for bag in rx.get("Data", {}).get("eff_order", []):
        for order in bag.get("order", []):

            # OMIF審查區間
            if order.get("CODE", "") == "OMIF":
                messages, error_type = omif_checker(order, messages, error_type, )

            # 管制藥品審查區間
            if "內用" not in order.get("TYPE", "") or order.get("DRUGKIND") == "N":
                return messages, error_type, error_rule
            messages, error_type, error_rule = insured_cannot_selfpay(order, bag, messages, error_type, error_rule)
            messages, error_type, error_rule = foreign_control_drug_limit(order, bag, messages, error_type, error_rule)
            messages, error_type, error_rule = foreign_max_days(order, bag, messages, error_type, error_rule)
            messages, error_type, error_rule = foreign_max_dosage(order, bag, messages, error_type, error_rule)
            messages, error_type, error_rule = doctor_cannot_prescribe_self(order, bag, messages, error_type, error_rule)

            # 口服藥品審查區間
            messages, error_type, error_rule = oral_drug_checker(order, messages, error_type, error_rule)

    return messages, error_type, error_rule