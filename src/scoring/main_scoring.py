from scorer import display_company_score, compare_all_scores

def main():
    print("=== Interface de Scoring - Agriculture ===")
    print("1. Évaluer une seule entreprise")
    print("2. Comparer visuellement toutes les entreprises")

    choice = input("Choisissez une option (1 ou 2) : ")
    if choice == "1":
        display_company_score()
    elif choice == "2":
        compare_all_scores()
    else:
        print("⛔ Option invalide.")

if __name__ == "__main__":
    main()