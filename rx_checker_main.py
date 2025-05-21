from sub_rules import *
from sub_tph_omif_checker import omif_checker

def main(rx, rule_state):
    error_type = []
    messages = []
    error_rule = []

    rule_functions = [
        oral_drug_checker,
        insured_cannot_selfpay,
        foreign_control_drug_limit,
        foreign_max_days,
        foreign_max_dosage,
        doctor_cannot_prescribe_self,
        omif_checker,
        diabetes_checker,
        airway_disease_checker
    ]

    for func in rule_functions:
        try:
            messages, error_type, error_rule = func(rule_state, rx, messages, error_type, error_rule)
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")

    return messages, error_type, error_rule