import os
import pandas as pd
from datetime import datetime
from data_generator import generate_company_data

def main():
    print("📊 Générateur de Données PME - Étude de Grâce PRASOC")

    min_budget = int(input("💰 Budget minimum PME ? "))
    max_budget = int(input("💰 Budget maximum PME ? "))
    max_interest = float(input("📈 Taux d'intérêt classique max (%) ? "))
    max_grace = int(input("⏳ Durée de grâce PRASOC max (années) ? "))

    companies = generate_company_data(
        min_budget=min_budget,
        max_budget=max_budget,
        max_interest=max_interest,
        max_grace=max_grace,
        n=20
    )

    df = pd.DataFrame(companies)

    # Ensure the data folder exists
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(data_dir, f"companies_{timestamp}.csv")

    # Save the file
    df.to_csv(file_path, index=False)
    print(f"\n✅ {len(companies)} PME générées et sauvegardées dans : {file_path}")

if __name__ == "__main__":
    main()
