import numpy as np
from typing import Tuple, List, Dict

def simulate_pme_growth(initial_revenue: float, params: Dict, years: int = 10) -> Tuple[List[float], bool]:
    """Simulate PME growth with given loan parameters"""
    revenue = initial_revenue
    revenue_history = [revenue]
    defaulted = False
    
    for year in range(years):
        if defaulted:
            revenue_history.append(0)
            continue
            
        # Simulate revenue growth with loan-specific parameters
        growth = np.random.normal(params['growth_mean'], params['growth_std'])
        revenue *= max(0.3, 1 + growth)
        revenue_history.append(revenue)
        
        # Check for default based on loan terms
        stress_factor = (1 + params['interest'] * 2) / (1 + params['grant'] * 10)
        default_prob = min(0.95, params['base_default'] * stress_factor)
        
        if revenue < initial_revenue * (0.7 - params['grace']*0.1):
            if np.random.random() < default_prob:
                defaulted = True
    
    return revenue_history, defaulted

def compare_loans(initial_revenue: float, prasoc_params: Dict, classic_params: Dict, 
                 years: int = 10, simulations: int = 200) -> Tuple[List, List]:
    """Compare two loan types"""
    prasoc_results = []
    classic_results = []
    
    for _ in range(simulations):
        # Simulate both loan types
        prasoc_growth, prasoc_default = simulate_pme_growth(initial_revenue, prasoc_params, years)
        classic_growth, classic_default = simulate_pme_growth(initial_revenue, classic_params, years)
        
        prasoc_results.append({
            'growth': prasoc_growth,
            'defaulted': prasoc_default,
            'final_revenue': 0 if prasoc_default else prasoc_growth[-1]
        })
        
        classic_results.append({
            'growth': classic_growth,
            'defaulted': classic_default,
            'final_revenue': 0 if classic_default else classic_growth[-1]
        })
    
    return prasoc_results, classic_results