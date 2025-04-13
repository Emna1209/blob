import numpy as np
from typing import List, Tuple, Union

def simulate_repayment(
    profit_path: Union[List[float], np.ndarray],
    loan_amount: float = 100000,
    interest_rate: float = 0.08,
    grace_period: int = 1,
    risk_profile: str = "medium"
) -> Tuple[List[float], bool]:
    """
    Simulates loan repayment for a PME with realistic default conditions
    
    Args:
        profit_path: Array-like of annual profits
        loan_amount: Total loan principal
        interest_rate: Annual interest rate
        grace_period: Years before repayment starts
        risk_profile: PME risk category
        
    Returns:
        Tuple of (repayment_schedule, default_status)
    """
    # Convert input to numpy array if needed
    if not isinstance(profit_path, np.ndarray):
        profit_path = np.array(profit_path)
    
    # Set risk parameters
    risk_params = {
        "low": {"miss_prob": 0.05, "default_threshold": 3},
        "medium": {"miss_prob": 0.15, "default_threshold": 2},
        "high": {"miss_prob": 0.25, "default_threshold": 1}
    }
    params = risk_params[risk_profile]
    
    total_due = loan_amount * (1 + interest_rate)
    repayment_years = len(profit_path) - grace_period
    annual_payment = total_due / repayment_years if repayment_years > 0 else 0
    
    repayments = []
    missed_payments = 0
    defaulted = False

    for i, profit in enumerate(profit_path):
        if defaulted:
            repayments.append(0)
            continue
            
        # Grace period handling
        if i < grace_period:
            repayments.append(0)
            continue
            
        # Ensure profit is a single value
        current_profit = float(profit) if isinstance(profit, (np.ndarray, list)) else profit
        
        # Determine repayment capacity
        max_repayment = current_profit * 0.3  # PMEs can allocate 30% of profits to debt
        
        # Random shock possibility
        if np.random.random() < params["miss_prob"]:
            repayment = 0
            missed_payments += 1
        else:
            repayment = min(max_repayment, annual_payment)
            # Reset missed payments counter if payment made
            if repayment >= annual_payment * 0.8:
                missed_payments = max(0, missed_payments - 1)
                
        # Default condition
        if missed_payments >= params["default_threshold"]:
            defaulted = True
            repayment = 0
            
        repayments.append(repayment)
    
    return repayments, defaulted

def simulate_portfolio_repayment(
    all_profits: List[List[float]],
    loan_amount: float,
    interest_rate: float,
    grace_period: int = 1,
    risk_profile: str = "medium"
) -> Tuple[np.ndarray, float]:
    """
    Simulates repayment for a portfolio of PMEs
    
    Returns:
        Tuple of (yearly_repayments, default_rate)
    """
    all_repayments = []
    defaults = 0
    
    for profit_path in all_profits:
        # Take first simulation path if multiple exist
        single_path = profit_path[0] if isinstance(profit_path[0], (list, np.ndarray)) else profit_path
        repayment, defaulted = simulate_repayment(
            single_path,
            loan_amount,
            interest_rate,
            grace_period,
            risk_profile
        )
        all_repayments.append(repayment)
        if defaulted:
            defaults += 1
            
    repayment_array = np.array(all_repayments)
    yearly_totals = repayment_array.sum(axis=0)
    default_rate = defaults / len(all_repayments)
    
    return yearly_totals, default_rate