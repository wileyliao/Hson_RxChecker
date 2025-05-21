from sub_rules import *
from sub_tph_omif_checker import omif_checker

def main(rx, rule_state):
    error_type = []
    messages = []
    error_rule = []

    messages, error_type, error_rule = oral_drug_checker(rule_state, rx, messages, error_type, error_rule)
    messages, error_type, error_rule = insured_cannot_selfpay(rule_state, rx, messages, error_type, error_rule)
    messages, error_type, error_rule = foreign_control_drug_limit(rule_state, rx, messages, error_type, error_rule)
    messages, error_type, error_rule = foreign_max_days(rule_state, rx, messages, error_type, error_rule)
    messages, error_type, error_rule = foreign_max_dosage(rule_state, rx, messages, error_type, error_rule)
    messages, error_type, error_rule = doctor_cannot_prescribe_self(rule_state, rx, messages, error_type, error_rule)

    messages, error_type, error_rule = omif_checker(rule_state, rx, messages, error_type, error_rule)

    messages, error_type, error_rule = diabetes_checker(rule_state, rx, messages, error_type, error_rule)
    messages, error_type, error_rule = airway_disease_checker(rule_state, rx, messages, error_type, error_rule)

    return messages, error_type, error_rule