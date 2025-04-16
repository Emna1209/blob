import pandas as pd
import matplotlib.pyplot as plt
import os


def simulate_loan_schedule(budget, interest_rate, grace_period=0, years=10, mode="classic"):
    schedule = []
    remaining = budget

    if mode == "classic":
        annual_principal = budget / years
    elif mode == "prasoc":
        pay_years = years - grace_period
        annual_principal = budget / pay_years if pay_years > 0 else 0

    for year in range(1, years + 1):
        if mode == "classic":
            interest = remaining * (interest_rate / 100)
            principal = annual_principal
            remaining -= principal

        elif mode == "prasoc":
            if year <= grace_period:
                interest = budget * (interest_rate / 100)  # Fixed interest during grace
                principal = 0
            else:
                interest = remaining * (interest_rate / 100)
                principal = annual_principal
                remaining -= principal

        if remaining < 0:
            remaining = 0

        total = principal + interest
        schedule.append([
            year,
            round(principal, 2),
            round(interest, 2),
            round(total, 2),
            round(remaining, 2)
        ])

    return schedule


def plot_comparative_table(name, classic_schedule, prasoc_schedule, initial_budget, loan_amount, classic_rate, prasoc_grace):
    headers = [
        "Year",
        "Classic Principal", "Classic Interest", "Classic Total", "Classic Remaining",
        "PRASOC Principal", "PRASOC Interest", "PRASOC Total", "PRASOC Remaining",
        "Budget"
    ]

    rows = []
    for i in range(len(classic_schedule)):
        row = classic_schedule[i][:] + prasoc_schedule[i][1:] + [initial_budget + loan_amount]
        rows.append(row)

    fig, ax = plt.subplots(figsize=(16, 0.6 * len(rows) + 2))
    ax.axis('off')
    ax.axis('tight')
    ax.set_title(f"📊 Simulation pour {name}", weight='bold', loc='center', fontsize=15, pad=20)    
    subtitle = (
        f"Montant Crédit: {loan_amount} TND\n"
        f"Budget Initial: {initial_budget} TND\n"
        f"Gràce PRASOC: {prasoc_grace} ans\n"
        f"Taux Classique: {classic_rate}% | Taux PRASOC: 8%"
    )
    ax.text(0.5, 1.02, subtitle, ha='center', va='top', transform=ax.transAxes, fontsize=12)
    
    table = ax.table(cellText=rows, colLabels=headers, loc='center', cellLoc='center')
    table.scale(1, 1.4)
    plt.tight_layout()
    plt.show()

    # Save to CSV
    os.makedirs("src/grace_effect/data/repayments", exist_ok=True)
    df = pd.DataFrame(rows, columns=headers)
    filepath = f"src/grace_effect/data/repayments/repayments_{name}.csv"
    df.to_csv(filepath, index=False)
    print(f"✅ Fichier exporté : {filepath}")


def generate_financial_tables_from_file(file_path):
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        name = row.get("Nom PME") or row.get("name", "PME")
        loan_amount = row["Montant Crédit"]
        classic_rate = int(row["Taux Intérêt Classique"])  # Ensure integer interest
        prasoc_grace = int(row["Période Grâce PRASOC"])
        initial_budget = row["Budget Initial"]

        classic = simulate_loan_schedule(loan_amount, classic_rate, grace_period=0, mode="classic")
        prasoc = simulate_loan_schedule(loan_amount, 8, grace_period=prasoc_grace, mode="prasoc")

        plot_comparative_table(name, classic, prasoc, initial_budget, loan_amount, classic_rate, prasoc_grace)
