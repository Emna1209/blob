import pandas as pd
from simulate import run_prasoc_simulations
from portfolio_metrics import summarize_portfolio
from scenarios import apply_stress_test
from visualize import (
    plot_total_recovery,
    plot_default_distribution,
    plot_repayment_distribution,
)
from core.config import LOAN_AMOUNT, INTEREST_PRASOC, YEARS


def load_mockup_data(path="data/mockup_data.xlsx"):
    df = pd.read_excel(path)
    df_latest = df.sort_values("Année").groupby("Nom PME").tail(1)
    return df_latest


def main():
    df = load_mockup_data()
    print("\n=== Analyse d'Impact BIAT - Ligne de Crédit PRASOC ===")
    print("1. 💵 Recouvrement Annuel Total")
    print("2. 🔥 Taux de défaut (défaillances)")
    print("3. 📊 Distribution des remboursements")
    print("4. 🌧️ Scénario stressé (choc économique)")
    print("5. 🧾 Résumé global du portefeuille")

    choice = input("\nChoisissez une option (1-5) : ")
    results = run_prasoc_simulations(df, LOAN_AMOUNT, INTEREST_PRASOC, YEARS)

    if choice == "1":
        plot_total_recovery(results, YEARS)

    elif choice == "2":
        plot_default_distribution(results)

    elif choice == "3":
        plot_repayment_distribution(results)

    elif choice == "4":
        stressed = apply_stress_test(results)
        print("\n\u26a1 Résultats après stress test:")
        plot_total_recovery(stressed, YEARS)
        plot_default_distribution(stressed)

    elif choice == "5":
        summary = summarize_portfolio(results)
        print("\n--- Résumé Portefeuille PRASOC ---")
        for key, value in summary.items():
            print(f"{key}: {value}")
    else:
        print("\n❌ Option invalide.")

if __name__ == "__main__":
    main()