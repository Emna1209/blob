import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.simulation import simulate_multiple_growth_paths
from core.repayment import simulate_repayment
from core.config import YEARS, N_SIMULATIONS
from prasoc_impact.visualize import (
    plot_profit_comparison,
    plot_biat_repayment_comparison
)


def simulate_loan_scenarios(base_profit):
    scenarios = {
        "prasoc": {
            "interest": 0.08,
            "grant": 0.14,
            "grace": 3,
        },
        "classic": {
            "interest": 0.12,
            "grant": 0.00,
            "grace": 1,
        }
    }

    output = {}

    for name, params in scenarios.items():
        profits = simulate_multiple_growth_paths(base_profit, N_SIMULATIONS, years=YEARS)
        repayments = [simulate_repayment(path,
                                          interest_rate=params["interest"],
                                          grant_rate=params["grant"],
                                          grace=params["grace"])
                      for path in profits]

        output[name] = {
            "profits": profits,
            "repayments": repayments
        }

    return output


def main():
    print("=== Comparaison Prêt PRASOC vs Prêt Classique ===")
    print("1. Évolution des bénéfices de l'entreprise")
    print("2. Remboursement total pour BIAT")

    choice = input("Choisissez une option (1 ou 2) : ")

    base_profit = 50000  # realistic base
    print(f"\n[ℹ️] Simulation avec bénéfice initial de {base_profit:,} TND...")

    result = simulate_loan_scenarios(base_profit)
    prosac_data = result["prasoc"]
    classic_data = result["classic"]

    if choice == "1":
        plot_profit_comparison(prosac_data["profits"], classic_data["profits"])
    elif choice == "2":
        plot_biat_repayment_comparison(prosac_data["repayments"], classic_data["repayments"])
    else:
        print("❌ Option invalide.")


if __name__ == "__main__":
    main()
