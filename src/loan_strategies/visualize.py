import matplotlib.pyplot as plt
import numpy as np

def plot_simulation_lines(prasoc_paths, classic_paths, title, ylabel):
    plt.figure(figsize=(10, 6))

    # Sample lines from each group
    for path in prasoc_paths[:100]:
        plt.plot(path, color='green', alpha=0.2)
    for path in classic_paths[:100]:
        plt.plot(path, color='orange', alpha=0.2)

    # Plot mean lines
    prasoc_mean = np.mean(prasoc_paths, axis=0)
    classic_mean = np.mean(classic_paths, axis=0)

    plt.plot(prasoc_mean, label="PRASOC (Avantage)", color="darkgreen", linewidth=2.5)
    plt.plot(classic_mean, label="Classique", color="darkorange", linewidth=2.5)

    plt.title(title)
    plt.xlabel("Années")
    plt.ylabel(ylabel)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()
