from simulator import simulate_loan_scenarios
from visualize import plot_profit_comparison, plot_biat_repayment_comparison

def main():
    print("=== Comparaison Prêt PRASOC vs Prêt Classique ===")
    print("1. Évolution des bénéfices de l'entreprise")
    print("2. Remboursement total pour BIAT")

    choice = input("Choisissez une option (1 ou 2) : ")

    base_profit = 50000  # set a fixed baseline to simulate all companies equally
    print(f"\n[ℹ️] Simulation avec un bénéfice initial de {base_profit:,} TND...")

    result = simulate_loan_scenarios(base_profit)
    prosac_data = result["prosac"]
    classic_data = result["classic"]

    if choice == "1":
        plot_profit_comparison(prosac_data["profits"], classic_data["profits"])
    elif choice == "2":
        plot_biat_repayment_comparison(prosac_data["repayments"], classic_data["repayments"])
    else:
        print("❌ Option invalide.")

if __name__ == "__main__":
    main()