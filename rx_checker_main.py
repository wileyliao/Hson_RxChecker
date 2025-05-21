from sub_rules import *
from sub_tph_omif_checker import omif_checker

def main(rx, rule_state):
    error_type = []
    messages = []
    error_rule = []

    messages, error_type, error_rule = oral_drug_checker(rx, messages, error_type, error_rule)
    messages, error_type, error_rule = insured_cannot_selfpay(rx, messages, error_type, error_rule)
    messages, error_type, error_rule = foreign_control_drug_limit(rx, messages, error_type, error_rule)
    messages, error_type, error_rule = foreign_max_days(rx, messages, error_type, error_rule)
    messages, error_type, error_rule = foreign_max_dosage(rx, messages, error_type, error_rule)
    messages, error_type, error_rule = doctor_cannot_prescribe_self(rx, messages, error_type, error_rule)

    messages, error_type, error_rule = omif_checker(rx, messages, error_type, error_rule)

    return messages, error_type, error_rule