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
    """Simulate PME revenue growth with Monte Carlo"""
    growth_mean = 0.06  # Average growth rate
    growth_std = 0.20   # Higher volatility for PMEs
    simulations = []

    for _ in range(n_simulations):
        value = net_income
        path = []
        for _ in range(n_years):
            # Simulate business growth with occasional crises
            if np.random.random() < 0.1:  # 10% chance of crisis year
                growth = np.random.normal(-0.15, 0.1)
            else:
                growth = np.random.normal(growth_mean, growth_std)
            
            value = max(value * 0.5, value * (1 + growth))  # Prevent complete collapse
            path.append(value)
        simulations.append(path)

    return simulations

def load_company_data() -> dict:
    """Load and prepare PME data"""
    try:
        df = pd.read_excel("data/mockup_data.xlsx")
        companies = df["Nom PME"].unique().tolist()
        
        # Get latest financials for each company
        latest_data = df.sort_values("Année").groupby("Nom PME").tail(1)
        return {
            company: latest_data[latest_data["Nom PME"] == company]["Résultat net (TND)"].values[0]
            for company in companies
        }
    except Exception as e:
        print(f"Error loading data: {e}")
        return {}

def main():
    print("=== Système d'Analyse de Prêts PME ===")
    print("1. Analyse individuelle d'une PME")
    print("2. Comparaison de toutes les PMEs")
    print("3. Analyse du portefeuille BIAT")
    print("4. Quitter")
    
    # Load data
    company_data = load_company_data()
    if not company_data:
        print("Erreur: Impossible de charger les données des PMEs")
        return
    
    # Prepare simulations
    all_results = {}
    for company, net_income in company_data.items():
        all_results[company] = simulate_profitability(net_income)
    
    while True:
        choice = input("\nChoisissez une option (1-4): ").strip()
        
        if choice == "1":
            # Individual company analysis
            print("\nPMEs disponibles:")
            for i, company in enumerate(company_data.keys(), 1):
                print(f"{i}. {company}")
                
            try:
                selection = int(input("Choisissez une PME: ")) - 1
                company = list(company_data.keys())[selection]
                plot_single_company(company, all_results[company])
                
                # Add repayment simulation
                loan_amount = float(input(f"Montant du prêt pour {company} (TND): ") or "100000")
                repayments, defaulted = simulate_repayment(
                    all_results[company][0],  # Use first simulation
                    loan_amount=loan_amount
                )
                print(f"\nRésultat du prêt:")
                print(f"- Default: {'Oui' if defaulted else 'Non'}")
                print(f"- Total remboursé: {sum(repayments):,.0f} TND")
                
            except (ValueError, IndexError):
                print("Selection invalide")
                
        elif choice == "2":
            # Comparison of all PMEs
            plot_average_comparison(all_results)
            
        elif choice == "3":
            # BIAT portfolio analysis
            print("\nParamètres du portefeuille:")
            loan_amount = float(input("Montant moyen par PME (TND): ") or "100000")
            interest_rate = float(input("Taux d'intérêt (%): ") or "8") / 100
            grace_period = int(input("Période de grâce (années): ") or "1")
            
            # Prepare profit paths - ensure we're passing single paths
            profit_paths = []
            for company_paths in all_results.values():
                # Take first simulation path for each company
                profit_paths.append(company_paths[0])
            
            # Run portfolio simulation
            yearly_totals, default_rate = simulate_portfolio_repayment(
                profit_paths,
                loan_amount=loan_amount,
                interest_rate=interest_rate,
                grace_period=grace_period
            )
            
            # Generate visualizations
            plot_biat_repayment_analysis(
                yearly_totals,
                loan_amount,
                interest_rate,
                len(company_data),
                default_rate
            )
            
            # Show repayment distribution
            sample_repayments = []
            for path in profit_paths[:100]:  # Sample 100 PMEs
                repayment, _ = simulate_repayment(
                    path,
                    loan_amount=loan_amount,
                    interest_rate=interest_rate,
                    grace_period=grace_period
                )
                sample_repayments.append(repayment)
            plot_repayment_distribution(sample_repayments)
                    
        elif choice == "4":
            print("Merci d'avoir utilisé le système d'analyse.")
            break
            
        else:
            print("Option invalide. Veuillez choisir 1-4.")

if __name__ == "__main__":
    main()