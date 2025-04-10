import matplotlib.pyplot as plt

def plot_profit_comparison(prosac, classic):
    years = list(range(1, len(prosac) + 1))
    plt.figure(figsize=(10, 6))
    plt.plot(years, prosac, label="PRASOC", color="green")
    plt.plot(years, classic, label="Classique", color="gray", linestyle="--")
    plt.title("Évolution des profits simulés")
    plt.xlabel("Années")
    plt.ylabel("Résultat Net (TND)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_biat_repayment_comparison(prosac, classic):
    years = list(range(1, len(prosac) + 1))
    plt.figure(figsize=(10, 6))
    plt.plot(years, prosac, label="Recouvrement PRASOC", color="green")
    plt.plot(years, classic, label="Recouvrement Classique", color="gray", linestyle="--")
    plt.title("Remboursements simulés à BIAT")
    plt.xlabel("Années")
    plt.ylabel("Montant remboursé (TND)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
