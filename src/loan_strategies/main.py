import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from loan_strategies.simulate import simulate_repayment_paths
from loan_strategies.visualize import plot_simulation_lines

YEARS = 10
SIMULATIONS = 300
START_PROFIT = 50000

def compare_grant():
    prasoc = simulate_repayment_paths(START_PROFIT, YEARS, SIMULATIONS, interest=0.08, grace=3, grant=0.14)
    classic = simulate_repayment_paths(START_PROFIT, YEARS, SIMULATIONS, interest=0.08, grace=3, grant=0.00)
    plot_simulation_lines(prasoc, classic, "🎁 Impact du Don (Grant 14%)", "Montant Remboursé (TND)")

def compare_interest():
    prasoc = simulate_repayment_paths(START_PROFIT, YEARS, SIMULATIONS, interest=0.08, grace=3, grant=0.00)
    classic = simulate_repayment_paths(START_PROFIT, YEARS, SIMULATIONS, interest=0.12, grace=3, grant=0.00)
    plot_simulation_lines(prasoc, classic, "📉 Impact du Taux d’Intérêt Réduit (8% vs 12%)", "Montant Remboursé (TND)")

def compare_grace():
    prasoc = simulate_repayment_paths(START_PROFIT, YEARS, SIMULATIONS, interest=0.08, grace=3, grant=0.00)
    classic = simulate_repayment_paths(START_PROFIT, YEARS, SIMULATIONS, interest=0.08, grace=1, grant=0.00)
    plot_simulation_lines(prasoc, classic, "⏳ Impact de la Période de Grâce (3 vs 1 an)", "Montant Remboursé (TND)")

def compare_combined():
    prasoc = simulate_repayment_paths(START_PROFIT, YEARS, SIMULATIONS, interest=0.08, grace=3, grant=0.14)
    classic = simulate_repayment_paths(START_PROFIT, YEARS, SIMULATIONS, interest=0.12, grace=1, grant=0.00)
    plot_simulation_lines(prasoc, classic, "🏆 Comparaison Globale PRASOC vs Classique", "Montant Remboursé (TND)")

def main():
    print("=== Comparaison Avantages PRASOC vs Crédit Classique ===")
    print("1. 🎁 Grant (don de 14%)")
    print("2. 📉 Taux d’intérêt réduit")
    print("3. ⏳ Période de grâce plus longue")
    print("4. 🏆 Comparaison globale (tout combiné)")

    choice = input("Choisissez une option (1 à 4) : ")

    if choice == "1":
        compare_grant()
    elif choice == "2":
        compare_interest()
    elif choice == "3":
        compare_grace()
    elif choice == "4":
        compare_combined()
    else:
        print("❌ Option invalide.")

if __name__ == "__main__":
    main()
