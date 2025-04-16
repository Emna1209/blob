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
    min_budget = int(input("💰 Minimum Budget? "))
    max_budget = int(input("💰 Maximum Budget? "))
    max_interest = int(input("📈 Max Classic Interest Rate (%)? "))
    max_grace = int(input("⏳ Max PRASOC Grace Period (years)? "))

    companies = generate_company_data(min_budget, max_budget, max_interest, max_grace)

    os.makedirs(DATA_FOLDER, exist_ok=True)
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"generated_pmes_{timestamp}.csv"
    output_path = os.path.join(DATA_FOLDER, filename)
    # Also save a shortcut to latest data
    latest_path = os.path.join(DATA_FOLDER, "generated_latest.csv")
    with open(latest_path, "w", newline="") as latest_file:
        writer = csv.DictWriter(latest_file, fieldnames=companies[0].keys())
        writer.writeheader()
        writer.writerows(companies)

    print(f"🧪 Shortcut saved as: {latest_path}")


    with open(output_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=companies[0].keys())
        writer.writeheader()
        writer.writerows(companies)

    print("✅ Data generated and saved.")

    # Display histogram
    df = pd.read_csv(output_path)
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8, 5))
    plt.hist(df["Loan Amount"], bins=10, color='skyblue', edgecolor='black')
    plt.title("Loan Amount Distribution\n✅ Generation Complete!")
    plt.xlabel("Loan Amount (TND)")
    plt.ylabel("Number of PMEs")
    plt.grid(axis='y', alpha=0.4)
    plt.tight_layout()
    plt.show()

def option_view_single_table():
    files = list_csv_files(DATA_FOLDER)
    if not files:
        print("❌ No CSV files found.")
        return

    print("\n📁 Available files:")
    for idx, file in enumerate(files):
        print(f"{idx+1}. {file}")

    choice = int(input("Choose a file: ")) - 1
    filepath = os.path.join(DATA_FOLDER, files[choice])
    df = pd.read_csv(filepath)

    print("\n📌 PMEs available:")
    for idx, name in enumerate(df["Company"]):
        print(f"{idx+1}. {name}")

    pme_choice = int(input("Choose a PME: ")) - 1
    selected_row = df.iloc[[pme_choice]]
    selected_row.to_csv("temp_selected_pme.csv", index=False)
    generate_financial_tables_from_file("temp_selected_pme.csv")
    os.remove("temp_selected_pme.csv")

def option_plot_budget():
    folder = "src/grace_effect/data/repayments"
    files = [f for f in os.listdir(folder) if f.endswith(".csv")]

    if not files:
        print("❌ No repayment files found.")
        return

    print("\n📁 Repayment files:")
    for idx, file in enumerate(files):
        print(f"{idx+1}. {file}")

    choice = int(input("Choose a file: ")) - 1
    if choice < 0 or choice >= len(files):
        print("❌ Invalid choice.")
        return

    growth_input = input("📈 Natural budget growth rate (%)? (default 3%) : ") or "3"
    growth_rate = float(growth_input) / 100

    filepath = os.path.join(folder, files[choice])
    plot_budget_evolution_from_csv(filepath, growth_rate)

def main():
    print("\n🎛️ Grace Effect Simulator")
    print("1. 🏗 Generate Test Data")
    print("2. 🧮 View Financial Table for a PME")
    print("3. 📉 Budget Evolution Simulation")

    option = input("Choose an option: ")

    if option == "1":
        option_generate_data()
    elif option == "2":
        option_view_single_table()
    elif option == "3":
        option_plot_budget()
    else:
        print("❌ Invalid option.")

if __name__ == "__main__":
    main()
