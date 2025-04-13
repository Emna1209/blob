import matplotlib.pyplot as plt
import numpy as np

def plot_growth_comparison(prasoc_results, classic_results, title, years):
    plt.figure(figsize=(14, 8))
    
    # Plot individual paths
    for result in prasoc_results[:100]:
        plt.plot(result['growth'], color='green', alpha=0.2 if result['defaulted'] else 0.4, linewidth=1)
    
    for result in classic_results[:100]:
        plt.plot(result['growth'], color='red', alpha=0.1 if result['defaulted'] else 0.3, linewidth=1)
    
    # Calculate and plot averages
    prasoc_avg = np.mean([r['growth'] for r in prasoc_results if not r['defaulted']] or [prasoc_results[0]['growth']], axis=0)
    classic_avg = np.mean([r['growth'] for r in classic_results if not r['defaulted']] or [classic_results[0]['growth']], axis=0)
    
    plt.plot(prasoc_avg, label="PRASOC (PME saines)", color='darkgreen', linewidth=3)
    plt.plot(classic_avg, label="Classique (PME saines)", color='darkred', linewidth=3, linestyle='--')
    
    # Add metrics
    prasoc_default_rate = sum(r['defaulted'] for r in prasoc_results)/len(prasoc_results)
    classic_default_rate = sum(r['defaulted'] for r in classic_results)/len(classic_results)
    
    plt.text(0.02, 0.95, 
             f"Défauts: PRASOC {prasoc_default_rate:.1%} | Classique {classic_default_rate:.1%}\n"
             f"Revenu final moyen: PRASOC {np.mean([r['final_revenue'] for r in prasoc_results]):,.0f} TND\n"
             f"Classique {np.mean([r['final_revenue'] for r in classic_results]):,.0f} TND",
             transform=plt.gca().transAxes,
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    
    plt.title(f"▲ {title} ▲\n{len(prasoc_results)} simulations", fontsize=16, pad=20)
    plt.xlabel("Années", fontsize=12)
    plt.ylabel("Revenu PME (TND)", fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.3)
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.show()