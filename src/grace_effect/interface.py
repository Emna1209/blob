import os
import pandas as pd
import csv
from data_generator import generate_company_data
from tables import generate_financial_tables_from_file
from budget_evolution import plot_budget_evolution_from_csv

DATA_FOLDER = "src/grace_effect/data"
REPAYMENT_FOLDER = os.path.join(DATA_FOLDER, "repayments")

def list_csv_files(folder):
    return [f for f in os.listdir(folder) if f.endswith(".csv")]

def option_generate_data():
    min_budget = int(input("💰 Budget minimum ? "))
    max_budget = int(input("💰 Budget maximum ? "))
    max_interest = int(input("📈 Taux d’intérêt classique max (%) ? "))
    max_grace = int(input("⏳ Durée de grâce PRASOC max (années) ? "))

    companies = generate_company_data(min_budget, max_budget, max_interest, max_grace)

    os.makedirs(DATA_FOLDER, exist_ok=True)
    filename = f"generated_{len(os.listdir(DATA_FOLDER)) + 1}.csv"
    filepath = os.path.join(DATA_FOLDER, filename)

    with open(filepath, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=companies[0].keys())
        writer.writeheader()
        writer.writerows(companies)

    print(f"\n✅ Données sauvegardées dans : {filepath}")

def option_view_single_table():
    files = list_csv_files(DATA_FOLDER)
    if not files:
        print("❌ Aucun fichier trouvé dans le dossier data.")
        return

    print("\n📁 Fichiers disponibles :")
    for idx, file in enumerate(files):
        print(f"{idx+1}. {file}")

    choice = int(input("Quel fichier voulez-vous utiliser ? ")) - 1
    if choice < 0 or choice >= len(files):
        print("❌ Choix invalide.")
        return

    filepath = os.path.join(DATA_FOLDER, files[choice])
    df = pd.read_csv(filepath)

    print("\n📌 PMEs disponibles :")
    for idx, name in enumerate(df["Nom PME"]):
        print(f"{idx+1}. {name}")

    pme_choice = int(input("Choisissez la PME à visualiser : ")) - 1
    if pme_choice < 0 or pme_choice >= len(df):
        print("❌ Choix invalide.")
        return

    selected_row = df.iloc[[pme_choice]]
    selected_row.to_csv("temp_selected_pme.csv", index=False)
    generate_financial_tables_from_file("temp_selected_pme.csv")
    os.remove("temp_selected_pme.csv")

def option_plot_budget():
    if not os.path.exists(REPAYMENT_FOLDER):
        print("❌ Aucun dossier de remboursement trouvé.")
        return

    files = list_csv_files(REPAYMENT_FOLDER)
    if not files:
        print("❌ Aucun fichier de remboursement trouvé.")
        return

    print("\n📁 Fichiers de remboursement disponibles :")
    for idx, file in enumerate(files):
        print(f"{idx+1}. {file}")

    choice = int(input("Quel fichier voulez-vous visualiser ? ")) - 1
    if choice < 0 or choice >= len(files):
        print("❌ Choix invalide.")
        return

    filepath = os.path.join(REPAYMENT_FOLDER, files[choice])
    plot_budget_evolution_from_csv(filepath)

def main():
    print("\n🎛️ Menu – Comparateur PRASOC vs Classique")
    print("1. 🎲 Générer des données de test")
    print("2. 🧮 Afficher le tableau financier pour une PME")
    print("3. 📈 Évolution du budget sous crédit (comparatif)")

    option = input("\nVotre choix ? ")

    if option == "1":
        option_generate_data()
    elif option == "2":
        option_view_single_table()
    elif option == "3":
        option_plot_budget()
    else:
        print("❌ Option invalide.")

if __name__ == "__main__":
    main()
