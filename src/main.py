import pandas as pd
import numpy as np
from visualize import plot_single_company, plot_average_comparison, plot_biat_revenue_forecast
from biat_projection import simulate_biat_returns
from repayment_model import simulate_repayment

def simulate_profitability(net_income, n_years=5, n_simulations=1000):
    growth_mean = 0.05
    growth_std = 0.10
    simulations = []

    for _ in range(n_simulations):
        path = []
        value = net_income

        for _ in range(n_years):
            growth = np.random.normal(loc=growth_mean, scale=growth_std)
            value = max(0, value * (1 + growth))  # Ensure no negative profits
            path.append(value)

        simulations.append(path)

    return simulations

def main():
    df = pd.read_excel("data/mockup_data.xlsx")
    companies = df["Nom PME"].unique().tolist()

    print("Bienvenue dans le simulateur de rentabilité 💸")
    print("1 - Focus sur une seule PME")
    print("2 - Comparaison de toutes les PME")
    print("3 - Voir impact sur BIAT 💰")
    mode = input("Choisissez une option (1, 2 ou 3) : ").strip()

    try:
        n_simulations = int(input("Nombre de simulations ? (défaut 1000) : ") or 1000)
        n_years = int(input("Horizon de prévision (en années, défaut 5) : ") or 5)
    except ValueError:
        print("Valeur invalide. Valeurs par défaut utilisées.")
        n_simulations, n_years = 1000, 5

    all_results = {}

    for company in companies:
        latest_row = df[df["Nom PME"] == company].sort_values("Année").iloc[-1]
        net_income = latest_row["Résultat net (TND)"]
        simulations = simulate_profitability(net_income, n_years=n_years, n_simulations=n_simulations)
        all_results[company] = simulations

    if mode == "1":
        print("\nPMEs disponibles :")
        for idx, name in enumerate(companies, start=1):
            print(f"{idx} - {name}")
        choice = int(input("Choisissez une PME à simuler : ")) - 1
        company = companies[choice]
        plot_single_company(company, all_results[company], years=n_years)

    elif mode == "2":
        plot_average_comparison(all_results, years=n_years)

    elif mode == "3":
        print("\n🧮 Simulation BIAT - Donnez 2 paramètres :")
        loan_amount = int(input("💰 Montant de prêt par PME (TND) ? ") or 100000)
        interest_rate = float(input("📈 Taux d’intérêt (%) ? ") or 7) / 100

        avg_cashflow, full_distribution = simulate_biat_returns(
            all_results,
            loan_amount=loan_amount,
            interest_rate=interest_rate
        )

        plot_biat_revenue_forecast(avg_cashflow, full_distribution, loan_amount, interest_rate)

if __name__ == "__main__":
    main()
