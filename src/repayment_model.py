import numpy as np
from typing import List, Tuple

def simulate_repayment(
    profit_path: List[float],
    loan_amount: float,
    interest_rate: float,
    grace_period: int = 1,
    min_repayment_ratio: float = 0.15
) -> Tuple[List[float], bool]:
    """
    Simulates loan repayment for a single PME with strict type checking
    """
    # Convert and validate inputs
    try:
        profit_path = [float(x) for x in profit_path]
        loan_amount = float(loan_amount)
        interest_rate = float(interest_rate)
        grace_period = int(grace_period)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid input type: {e}")

    total_due = loan_amount * (1 + interest_rate)
    repayment_years = max(1, len(profit_path) - grace_period)
    annual_payment = total_due / repayment_years
    
    repayments = []
    missed_payments = 0
    defaulted = False

    for i, profit in enumerate(profit_path):
        if defaulted:
            repayments.append(0.0)
            continue
            
        if i < grace_period:
            repayments.append(0.0)
            continue
            
        # Calculate repayment with safeguards
        try:
            repayment_capacity = min(float(profit) * 0.3, annual_payment)
            min_required = annual_payment * min_repayment_ratio
            
            if repayment_capacity >= min_required:
                repayment = min(repayment_capacity, annual_payment)
                missed_payments = max(0, missed_payments - 1)
            else:
                repayment = min_required
                missed_payments += 1
                
            if missed_payments >= 2:
                defaulted = True
                repayment = 0.0
                
            repayments.append(float(repayment))
        except Exception as e:
            raise ValueError(f"Repayment calculation error at year {i}: {e}")
    
    return repayments, defaulted

def simulate_portfolio_repayment(
    all_profits: List[List[float]],
    loan_amount: float,
    interest_rate: float,
    grace_period: int = 1
) -> Tuple[np.ndarray, float]:
    """
    Simulates repayment for a portfolio of PMEs with strict type checking
    """
    # Validate inputs
    if not all_profits or not isinstance(all_profits[0], (list, np.ndarray)):
        raise ValueError("Invalid profit paths format")
    
    all_repayments = []
    defaults = 0
    
    for profit_path in all_profits:
        try:
            # Take first path if multiple exist
            single_path = profit_path[0] if isinstance(profit_path[0], (list, np.ndarray)) else profit_path
            single_path = [float(x) for x in single_path]
            
            repayment, defaulted = simulate_repayment(
                single_path,
                loan_amount,
                interest_rate,
                grace_period
            )
            all_repayments.append(repayment)
            defaults += 1 if defaulted else 0
        except Exception as e:
            raise ValueError(f"Error processing PME: {e}")
    
    try:
        repayment_array = np.array(all_repayments, dtype=float)
        yearly_totals = repayment_array.sum(axis=0)
        default_rate = defaults / len(all_repayments)
        return yearly_totals, default_rate
    except Exception as e:
        raise ValueError(f"Portfolio aggregation error: {e}")