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

def plot_biat_revenue_forecast(cashflow_array, full_distribution, loan_amount, interest_rate):
    plt.figure(figsize=(13, 7))
    full_distribution = np.array(full_distribution)

    mean = full_distribution.mean(axis=0)
    p5 = np.percentile(full_distribution, 5, axis=0)
    p95 = np.percentile(full_distribution, 95, axis=0)
    years = range(1, len(mean) + 1)

    for sim in full_distribution[:150]:
        plt.plot(years, sim, color='lightgray', linewidth=0.6, alpha=0.4)

    plt.fill_between(years, p5, p95, color='lightgreen', alpha=0.3, label='Intervalle 5e–95e percentile')
    plt.plot(years, mean, color='darkgreen', linewidth=2.5, label='Remboursement moyen')

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

def plot_group_comparison(stable_avg, risky_avg, years):
    plt.figure(figsize=(10, 6))
    x = range(1, years + 1)
    plt.plot(x, stable_avg, label='PMEs Stables', color='green', linewidth=2.5)
    plt.plot(x, risky_avg, label='PMEs à Risque', color='red', linewidth=2.5)

    plt.fill_between(x, stable_avg, risky_avg, where=(np.array(risky_avg) < np.array(stable_avg)), color='lightcoral', alpha=0.2, label="Manque à gagner")
    plt.title("Comparaison des remboursements moyens - Stables vs Risqués")
    plt.xlabel("Années")
    plt.ylabel("Remboursement annuel moyen (TND)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_group_comparison(stable_paths, risky_paths, stable_avg, risky_avg, years=5):
    months = range(1, years + 1)

    plt.figure(figsize=(14, 6))

    
    plt.subplot(1, 2, 1)
    for path in np.array(stable_paths)[:100]:
        plt.plot(months, path, color='skyblue', alpha=0.4)
    plt.plot(months, stable_avg, color='blue', linewidth=2.5, label='Moyenne')
    plt.fill_between(months,
                     np.percentile(stable_paths, 10, axis=0),
                     np.percentile(stable_paths, 90, axis=0),
                     color='blue', alpha=0.1)
    plt.title("PMEs Stables")
    plt.xlabel("Années")
    plt.ylabel("Part du prêt remboursé")
    plt.ylim(0, 1.05)
    plt.legend()

    
    plt.subplot(1, 2, 2)
    for path in np.array(risky_paths)[:100]:
        plt.plot(months, path, color='salmon', alpha=0.4)
    plt.plot(months, risky_avg, color='red', linewidth=2.5, label='Moyenne')
    plt.fill_between(months,
                     np.percentile(risky_paths, 10, axis=0),
                     np.percentile(risky_paths, 90, axis=0),
                     color='red', alpha=0.1)
    plt.title("PMEs à Risque")
    plt.xlabel("Années")
    plt.ylim(0, 1.05)
    plt.legend()

    plt.tight_layout()
    plt.show()

def plot_biat_repayment_analysis(yearly_totals: np.ndarray,
                               loan_amount: float,
                               interest_rate: float,
                               n_pmes: int,
                               default_rate: float):
    """
    Shows BIAT's expected repayment from PME portfolio
    """
    plt.figure(figsize=(14, 7))
    
    # Calculate metrics
    total_loan = loan_amount * n_pmes
    expected_return = yearly_totals.sum()
    roi = (expected_return - total_loan) / total_loan
    
    # Create plot
    years = range(1, len(yearly_totals) + 1)
    plt.bar(years, yearly_totals, color='#1f77b4', alpha=0.7, label='Remboursements annuels')
    
    # Add reference lines
    plt.axhline(y=total_loan, color='r', linestyle='--', label='Capital prêté')
    plt.axhline(y=expected_return, color='g', linestyle=':', label='Total attendu')
    
    # Formatting
    plt.title(
        f"Projection BIAT - Portefeuille PME\n"
        f"{n_pmes} PMEs × {loan_amount:,.0f} TND à {interest_rate*100:.1f}%\n"
        f"ROI: {roi:.1%} | Défauts: {default_rate:.1%}",
        fontsize=14, pad=20
    )
    plt.xlabel("Années")
    plt.ylabel("Remboursements totaux (TND)")
    plt.legend()
    plt.grid(True, axis='y', alpha=0.3)
    
    # Add table with key metrics
    metrics = [
        ["Capital prêté", f"{total_loan:,.0f} TND"],
        ["Total attendu", f"{expected_return:,.0f} TND"],
        ["ROI projeté", f"{roi:.1%}"],
        ["Taux de défaut", f"{default_rate:.1%}"],
        ["Durée moyenne", f"{len(years)} ans"]
    ]
    
    plt.table(
        cellText=metrics,
        colLabels=["Métrique", "Valeur"],
        loc='bottom',
        bbox=[0, -0.3, 1, 0.3]
    )
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.3)
    plt.show()

def plot_repayment_distribution(repayment_paths: list[list[float]]):
    """Show distribution of repayment outcomes"""
    plt.figure(figsize=(12, 6))
    
    # Calculate statistics
    final_repayments = [sum(path) for path in repayment_paths]
    avg_repayment = np.mean(final_repayments)
    
    # Plot histogram
    plt.hist(final_repayments, bins=30, color='skyblue', edgecolor='white', alpha=0.7)
    plt.axvline(avg_repayment, color='red', linestyle='--', label=f'Moyenne: {avg_repayment:,.0f} TND')
    
    # Formatting
    plt.title("Distribution des Remboursements Totaux par PME")
    plt.xlabel("Montant total remboursé (TND)")
    plt.ylabel("Nombre de PMEs")
    plt.legend()
    plt.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()