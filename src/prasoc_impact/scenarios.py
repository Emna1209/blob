from core.repayment import simulate_repayment

def apply_stress_test(simulated_results, stress_factor=0.7):
    stressed = []
    for entry in simulated_results:
        stressed_path = [val * stress_factor for val in entry["profit_path"]]
        new_repayment = simulate_repayment(stressed_path)
        stressed.append({
            **entry,
            "repayment_path": new_repayment,
            "total_repaid": sum(new_repayment),
            "defaulted": sum(new_repayment) < 60000
        })
    return stressed
