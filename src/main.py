import pandas as pd
import numpy as np
from visualize import (
    plot_single_company, 
    plot_average_comparison,
    plot_biat_repayment_analysis,
    plot_repayment_distribution
)
from repayment_model import (
    simulate_repayment,
    simulate_portfolio_repayment
)

def simulate_profitability(net_income: float, n_years: int = 5, n_simulations: int = 1000) -> list:
    """Simulates PME revenue growth with Monte Carlo"""
    simulations = []
    for _ in range(n_simulations):
        value = float(net_income)
        path = []
        for _ in range(n_years):
            growth = np.random.normal(0.06, 0.15)  # 6% mean growth, 15% std
            value = max(value * 0.5, value * (1 + growth))  # Prevent complete collapse
            path.append(float(value))
        simulations.append(path)
    return simulations

def load_company_data() -> dict:
    """Loads and prepares PME data with validation"""
    try:
        df = pd.read_excel("data/mockup_data.xlsx")
        df.columns = df.columns.str.strip()  # Remove extra whitespace from headers

        # Optional: print to verify column names
        print("Columns:", df.columns.tolist())

        # Group by 'Nom PME' and get the latest year per company
        latest_data = df.sort_values("Année").groupby("Nom PME").last()

        # Extract the result
        company_data = {
            row["Nom PME"]: float(row["Résultat net (TND)"])
            for _, row in latest_data.reset_index().iterrows()
        }

        return company_data

    except Exception as e:
        print(f"Error loading data: {e}")
        return {}
    
def main():
    print("=== Système d'Analyse de Prêts PME ===")
    print("1. Analyse individuelle d'une PME")
    print("2. Comparaison de toutes les PMEs")
    print("3. Analyse du portefeuille BIAT")
    print("4. Quitter")
    
    # Load and validate data
    company_data = load_company_data()
    if not company_data:
        print("Erreur: Aucune donnée PME valide trouvée")
        return
    
    # Run simulations
    all_results = {
        company: simulate_profitability(net_income)
        for company, net_income in company_data.items()
    }

    while True:
        try:
            choice = input("\nChoisissez une option (1-4): ").strip()
            
            if choice == "1":
                # Individual PME analysis
                print("\nPMEs disponibles:")
                for i, company in enumerate(company_data.keys(), 1):
                    print(f"{i}. {company}")
                
                try:
                    selection = int(input("Choisissez une PME: ")) - 1
                    company = list(company_data.keys())[selection]
                    plot_single_company(company, all_results[company])
                    
                    loan_amount = float(input(f"Montant du prêt pour {company} (TND): ") or "100000")
                    interest_rate = float(input("Taux d'intérêt (%): ") or "8") / 100
                    
                    repayments, defaulted = simulate_repayment(
                        all_results[company][0],
                        loan_amount,
                        interest_rate
                    )
                    print(f"\nRésultat du prêt:")
                    print(f"- Default: {'Oui' if defaulted else 'Non'}")
                    print(f"- Total remboursé: {sum(repayments):,.0f} TND")
                    
                except (ValueError, IndexError) as e:
                    print(f"Erreur: {e}")
                    
            elif choice == "2":
                # Comparison of all PMEs
                plot_average_comparison(all_results)
                
            elif choice == "3":
                # BIAT portfolio analysis
                print("\n=== Analyse Portefeuille BIAT ===")
                loan_amount = float(input("Montant moyen par PME (TND): ") or "100000")
                interest_rate = float(input("Taux d'intérêt (%): ") or "8") / 100
                grace_period = min(int(input("Période de grâce (années, max 3): ") or "1"), 3)
                
                # Prepare and validate profit paths
                profit_paths = []
                for company in company_data:
                    try:
                        profit_paths.append([float(x) for x in all_results[company][0]])
                    except Exception as e:
                        print(f"Erreur dans les données de {company}: {e}")
                        continue
                
                if not profit_paths:
                    print("Aucune donnée valide pour l'analyse")
                    continue
                
                # Run portfolio simulation
                yearly_totals, default_rate = simulate_portfolio_repayment(
                    profit_paths,
                    loan_amount,
                    interest_rate,
                    grace_period
                )
                
                # Calculate and validate ROI
                total_loan = loan_amount * len(profit_paths)
                total_expected = sum(yearly_totals)
                roi = (total_expected - total_loan) / total_loan
                
                if roi < 0:
                    print("Attention: ROI négatif détecté - vérifiez les paramètres")
                
                # Visualization
                plot_biat_repayment_analysis(
                    yearly_totals,
                    loan_amount,
                    interest_rate,
                    len(profit_paths),
                    default_rate
                )
                
                # Show repayment distribution
                sample_repayments = []
                for path in profit_paths[:100]:
                    try:
                        repayment, _ = simulate_repayment(
                            path,
                            loan_amount,
                            interest_rate,
                            grace_period
                        )
                        sample_repayments.append(repayment)
                    except Exception as e:
                        print(f"Erreur dans la simulation: {e}")
                
                if sample_repayments:
                    plot_repayment_distribution(sample_repayments)
                else:
                    print("Aucune donnée valide pour la distribution")
                    
            elif choice == "4":
                print("Merci d'avoir utilisé le système d'analyse.")
                break
                
            else:
                print("Option invalide. Veuillez choisir 1-4.")
                
        except Exception as e:
            print(f"Erreur inattendue: {e}")

if __name__ == "__main__":
    main()