from simulate import compare_loans
from visualize import plot_growth_comparison

YEARS = 10
SIMULATIONS = 200
INITIAL_REVENUE = 50000

# Loan parameters
BASE_PARAMS = {
    'prasoc': {
        'growth_mean': 0.08,
        'growth_std': 0.12,
        'base_default': 0.05,
        'interest': 0.08,
        'grace': 3,
        'grant': 0.14
    },
    'classical': {
        'growth_mean': 0.05,
        'growth_std': 0.18,
        'base_default': 0.15,
        'interest': 0.12,
        'grace': 1,
        'grant': 0.00
    }
}

def run_comparison(title, prasoc_params, classic_params):
    prasoc_results, classic_results = compare_loans(
        INITIAL_REVENUE, prasoc_params, classic_params, YEARS, SIMULATIONS)
    plot_growth_comparison(prasoc_results, classic_results, title, YEARS)

def main():
    while True:
        print("\n=== Analyse Avantages PRASOC ===")
        print("1. 🎁 Impact du don de 14%")
        print("2. 📉 Avantage du taux réduit (8% vs 12%)")
        print("3. ⏳ Période de grâce étendue (3 ans vs 1 an)")
        print("4. 🏆 Avantage combiné complet")
        print("5. 🚪 Quitter")
        
        choice = input("Choix (1-5): ").strip()
        
        if choice == "1":
            prasoc = BASE_PARAMS['prasoc'].copy()
            classic = BASE_PARAMS['classical'].copy()
            classic.update({'grant': 0.14})  # Compare grant impact
            run_comparison("Impact du Don de 14%", prasoc, classic)
            
        elif choice == "2":
            prasoc = BASE_PARAMS['prasoc'].copy()
            classic = BASE_PARAMS['classical'].copy()
            classic.update({'interest': 0.08})  # Compare interest impact
            run_comparison("Taux Réduit (8% vs 12%)", prasoc, classic)
            
        elif choice == "3":
            prasoc = BASE_PARAMS['prasoc'].copy()
            classic = BASE_PARAMS['classical'].copy()
            classic.update({'grace': 3})  # Compare grace period
            run_comparison("Période de Grâce (3 ans vs 1 an)", prasoc, classic)
            
        elif choice == "4":
            run_comparison("Avantage Combiné PRASOC", 
                          BASE_PARAMS['prasoc'], 
                          BASE_PARAMS['classical'])
            
        elif choice == "5":
            print("Merci d'avoir utilisé l'analyse PRASOC!")
            break
            
        else:
            print("❌ Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()