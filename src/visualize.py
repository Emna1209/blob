import matplotlib.pyplot as plt
import numpy as np

def plot_single_company(company_name, simulations, years=5, n_samples=100):
    plt.figure(figsize=(10, 6))
    simulations = np.array(simulations)
    for i in range(min(n_samples, simulations.shape[0])):
        plt.plot(range(1, years + 1), simulations[i], color='lightgray', linewidth=0.7)
    avg = simulations.mean(axis=0)
    plt.plot(range(1, years + 1), avg, color='blue', linewidth=2, label='Moyenne')
    plt.title(f"{company_name} - Simulation de Rentabilité")
    plt.xlabel("Années")
    plt.ylabel("Résultat Net (TND)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_average_comparison(all_results, years=5):
    plt.figure(figsize=(12, 7))
    for company_name, simulations in all_results.items():
        simulations = np.array(simulations)
        mean_path = simulations.mean(axis=0)
        plt.plot(range(1, years + 1), mean_path, label=company_name)
    plt.title("Comparaison des Moyennes - Simulation de Rentabilité")
    plt.xlabel("Années")
    plt.ylabel("Résultat Net (TND)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

import matplotlib.pyplot as plt
import numpy as np

def plot_biat_revenue_forecast(cashflow_array, full_distribution, loan_amount, interest_rate):
    plt.figure(figsize=(13, 7))
    full_distribution = np.array(full_distribution)

    mean = full_distribution.mean(axis=0)
    p5 = np.percentile(full_distribution, 5, axis=0)
    p95 = np.percentile(full_distribution, 95, axis=0)
    years = range(1, len(mean) + 1)

    # ✅ Show 150 simulation paths (rain effect)
    sample_size = min(150, len(full_distribution))
    for sim in full_distribution[:150]:  # Just take the first 150
        plt.plot(years, sim, color='lightgray', linewidth=0.6, alpha=0.4)

    # ✅ Confidence band
    plt.fill_between(years, p5, p95, color='lightgreen', alpha=0.3, label='Intervalle 5e–95e percentile')

    # ✅ Average line
    plt.plot(years, mean, color='darkgreen', linewidth=2.5, label='Remboursement moyen')

    # ✅ Title and layout (no emojis)
    total = int(sum(mean))
    plt.title(
        f"Prévision BIAT: {loan_amount:,} TND / PME à {interest_rate*100:.1f}% intérêt\n"
        f"Total moyen récupéré sur {len(mean)} ans ≈ {total:,} TND",
        fontsize=14
    )
    plt.xlabel("Années")
    plt.ylabel("Remboursement annuel (TND)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
