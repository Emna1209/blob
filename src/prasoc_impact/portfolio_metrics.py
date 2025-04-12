def summarize_portfolio(simulated_results):
    total_loans = len(simulated_results)
    total_repaid = sum(r["total_repaid"] for r in simulated_results)
    defaults = sum(1 for r in simulated_results if r["defaulted"])

    avg_repaid = total_repaid / total_loans if total_loans else 0
    default_rate = defaults / total_loans if total_loans else 0

    return {
        "total_loans": total_loans,
        "total_repaid": round(total_repaid, 2),
        "avg_repaid": round(avg_repaid, 2),
        "default_rate": round(default_rate * 100, 2),
    }