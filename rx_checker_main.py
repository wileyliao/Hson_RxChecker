from sub_rules_adc import *
from sub_rules_oral import *
from sub_rules_omif import *
from sub_rules_clinical import *
from log_generate import generate_log

def main(rx, rule_state, rule_state_duration):
    error_type, messages, error_rule = [], [], []

    rule_functions = [
        oral_drug_checker,
        insured_cannot_selfpay,
        foreign_control_drug_limit,
        foreign_max_days,
        foreign_max_dosage,
        doctor_cannot_prescribe_self,
        omif_checker,
        diabetes_checker,
        airway_disease_checker,
        pregnancy_drug_risk
    ]

    for func in rule_functions:
        try:
            messages, error_type, error_rule = func(rule_state, rx, messages, error_type, error_rule)
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")

    triggered_rules = set(error_rule)

    log_data = generate_log(rx, triggered_rules, rule_state, rule_state_duration)
    return messages, error_type, error_rule, log_data
