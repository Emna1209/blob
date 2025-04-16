import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_budget_evolution_from_csv(filepath):
    df = pd.read_csv(filepath)

    # Extract initial budget (same across all rows)
    initial_budget = df["Budget Initial"].iloc[0]

    # Calculate yearly remaining budget
    budget_classic = []
    budget_prasoc = []

    current_classic = initial_budget
    current_prasoc = initial_budget

    for i in range(len(df)):
        classic_payment = df.iloc[i]["Classic Total"]
        prasoc_payment = df.iloc[i]["PRASOC Total"]

        current_classic -= classic_payment
        current_prasoc -= prasoc_payment

        budget_classic.append(round(current_classic, 2))
        budget_prasoc.append(round(current_prasoc, 2))

    # Plotting
    years = df["Year"]
    name = os.path.basename(filepath).replace("repayments_", "").replace(".csv", "")

    plt.figure(figsize=(10, 5))
    plt.plot(years, budget_classic, label="Classique", marker='o', color='orange')
    plt.plot(years, budget_prasoc, label="PRASOC", marker='o', color='green')
    plt.title(f"💰 Évolution du Budget - {name}")
    plt.xlabel("Année")
    plt.ylabel("Budget Restant (TND)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()
