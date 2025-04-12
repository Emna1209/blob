import matplotlib.pyplot as plt

def plot_total_recovery(simulated_results, years):
    yearly_totals = [0] * years
    for result in simulated_results:
        for i in range(min(years, len(result["repayment_path"]))):
            yearly_totals[i] += result["repayment_path"][i]

    plt.figure(figsize=(10, 5))
    plt.plot(range(1, years + 1), yearly_totals, marker='o', color='green', linewidth=2)
    plt.title("Recouvrement Annuel Total de BIAT (Ligne PRASOC)")
    plt.xlabel("Années")
    plt.ylabel("Montant Remboursé (TND)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_default_distribution(simulated_results):
    defaulted = sum(1 for r in simulated_results if r["defaulted"])
    not_defaulted = len(simulated_results) - defaulted

    plt.figure(figsize=(6, 6))
    plt.pie([not_defaulted, defaulted], labels=["Saines", "Défaillantes"], autopct="%1.1f%%",
            colors=["#8bc34a", "#e57373"], startangle=140)
    plt.title("Répartition des Entreprises selon Défaut")
    plt.tight_layout()
    plt.show()

def plot_repayment_distribution(simulated_results):
    values = [r["total_repaid"] for r in simulated_results]
    plt.figure(figsize=(9, 5))
    plt.hist(values, bins=20, color='skyblue', edgecolor='black')
    plt.title("Distribution des Montants Remboursés (PRASOC)")
    plt.xlabel("Montant total remboursé par entreprise (TND)")
    plt.ylabel("Nombre d'observations")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()