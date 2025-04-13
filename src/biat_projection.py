import numpy as np
from typing import Dict, List, Tuple

def simulate_pme_repayment(profit_path: List[float], 
                          loan_amount: float,
                          interest_rate: float,
                          grace_period: int = 1) -> Tuple[List[float], bool]:
    """
    Simulates repayment behavior for a single PME
    Returns: (repayment_path, default_status)
    """
    total_due = loan_amount * (1 + interest_rate)
    annual_payment = total_due / (len(profit_path) - grace_period)
    repayments = []
    missed_payments = 0
    defaulted = False
    
    for i, profit in enumerate(profit_path):
        if defaulted:
            repayments.append(0)
            continue
            
        # Grace period
        if i < grace_period:
            repayments.append(0)
            continue
            
        # Determine repayment capacity
        max_repayment = profit * 0.3  # PMEs can allocate 30% of profits
        actual_repayment = min(max_repayment, annual_payment)
        
        # Random shock possibility
        if np.random.random() < 0.05:  # 5% chance of external shock
            actual_repayment *= np.random.uniform(0.1, 0.8)
            
        # Default condition
        if actual_repayment < annual_payment * 0.5:
            missed_payments += 1
            if missed_payments >= 2:
                defaulted = True
                actual_repayment = 0
                
        repayments.append(actual_repayment)
    
    return repayments, defaulted

def simulate_biat_portfolio(pme_profits: Dict[str, List[List[float]]],
                          loan_amount: float,
                          interest_rate: float,
                          grace_period: int = 1) -> Tuple[np.ndarray, float]:
    """
    Simulates repayment for BIAT's entire PME portfolio
    Returns: (yearly_cashflows, default_rate)
    """
    all_cashflows = []
    defaults = 0
    
    for company in pme_profits.values():
        for profit_path in company:
            repayment, defaulted = simulate_pme_repayment(
                profit_path, loan_amount, interest_rate, grace_period
            )
            all_cashflows.append(repayment)
            if defaulted:
                defaults += 1
                
    # Convert to numpy array and sum across PMEs
    cashflow_array = np.array(all_cashflows)
    yearly_totals = cashflow_array.sum(axis=0)
    
    default_rate = defaults / len(all_cashflows)
    return yearly_totals, default_rate