import matplotlib.pyplot as plt
import numpy as np

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

def plot_profit_comparison(prasoc_profits, classic_profits):
    import numpy as np
    prasoc_avg = np.mean(prasoc_profits, axis=0)
    classic_avg = np.mean(classic_profits, axis=0)
    x = range(1, len(prasoc_avg) + 1)

    plt.plot(x, prasoc_avg, label="PRASOC", color="green")
    plt.plot(x, classic_avg, label="Classique", color="orange")
    plt.title("Évolution moyenne des bénéfices")
    plt.xlabel("Années")
    plt.ylabel("Bénéfice annuel (TND)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_biat_repayment_comparison(prasoc_repayments, classic_repayments):
    prasoc_sum = np.sum(prasoc_repayments, axis=1)
    classic_sum = np.sum(classic_repayments, axis=1)

    plt.boxplot([prasoc_sum, classic_sum], labels=["PRASOC", "Classique"])
    plt.title("Montant total remboursé à BIAT")
    plt.ylabel("TND")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
