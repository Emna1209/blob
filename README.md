# PRASOC Loan Simulation for BIAT

This project simulates how PRASOC loans given to different types of SMEs affect repayment performance at BIAT. It compares stable vs. high-potential companies using Monte Carlo simulations, displaying repayment trends and risks.

## 🔧 Installation

Clone this repository, navigate to the project directory, and install the required packages:

```bash
git clone <your_repo_url>
cd project
pip install -r requirements.txt

import os

# Create directory and files for the new scoring interface
base_path = "project/src/scoring"
os.makedirs(base_path, exist_ok=True)

# Create file stubs with starter content
files = {
    "main_scoring.py": """\
from scorer import calculate_scores
from score_compare import compare_scores
from score_growth import simulate_score_growth

def main():
    print("=== Interface de Scoring PME AGRI ===")
    print("1. Calculer le score d'une entreprise")
    print("2. Comparer plusieurs entreprises")
    print("3. Simuler l’évolution d’un score")
    choice = input("Choisissez une option (1, 2 ou 3): ")

    if choice == "1":
        calculate_scores()
    elif choice == "2":
        compare_scores()
    elif choice == "3":
        simulate_score_growth()
    else:
        print("Option invalide.")

if __name__ == "__main__":
    main()
""",

    "scorer.py": """\
import pandas as pd
import json
from score_utils import parse_json_column

def calculate_scores():
    print("\\n🔍 Calcul du score pour une entreprise...")
    file_path = "data/mockup_agriculture_messy_keyvalue.xlsx"
    df = pd.read_excel(file_path)

    company_name = input("Nom de la PME ? ")
    row = df[df["Nom PME"] == company_name].squeeze()

    if row.empty:
        print("PME non trouvée.")
        return

    ca = parse_json_column(row["Chiffres_Affaires"])
    charges = parse_json_column(row["Charges"])
    prix_produits = parse_json_column(row["Prix_Produits"])
    prix_marche = parse_json_column(row["Prix_Marche"])

    # TODO: Add real scoring logic per ECO1–ECO4
    print(f"➡️ Chiffres d'affaires : {ca}")
    print(f"➡️ Charges : {charges}")
    print(f"➡️ Prix Produits : {prix_produits}")
    print(f"➡️ Prix Marché : {prix_marche}")
    print(f"➡️ Nb Produits : {row['Nb_produits']}")
    print(f"➡️ Ratio dépendance : {row['Ratio_dependance']}")
    print(f"➡️ Ratio assurance : {row['Ratio_assurance']}")

    # Simulate a mock score
    print(f"✅ Score simulé pour {company_name} : 22 / 40")
""",

    "score_utils.py": """\
import json

def parse_json_column(cell):
    try:
        return json.loads(cell)
    except Exception as e:
        print(f"[!] Erreur de parsing JSON: {e}")
        return []
""",

    "score_compare.py": """\
def compare_scores():
    print("\\n📊 Comparaison des scores entre entreprises...")
    # TODO: Implement comparison logic
""",

    "score_growth.py": """\
def simulate_score_growth():
    print("\\n📈 Simulation d’évolution du score...")
    # TODO: Implement score growth logic
"""
}

# Write files to the scoring directory
for filename, content in files.items():
    with open(os.path.join(base_path, filename), "w", encoding="utf-8") as f:
        f.write(content)

"Scoring interface scaffolded successfully in src/scoring/"
