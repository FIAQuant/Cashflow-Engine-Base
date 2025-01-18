import numpy as np

class CashflowCalculator:
    """
    Base class for shared cashflow calculations.
    """

    def calculate_present_value(self, cashflows, discount_rate, payment_frequency=1):
        """
        Calculate the present value (PV) of a bond given its cashflows and a discount rate.

        Parameters:
        - cashflows (list of floats): List of cashflows for the bond.
        - discount_rate (float): Annual discount rate as a decimal (e.g., 0.04 for 4%).
        - payment_frequency (int): Number of coupon payments per year (e.g., 1 for annual, 2 for semiannual).

        Returns:
        - float: The present value (PV) of the bond.
        """
        period_discount_rate = discount_rate / payment_frequency
        pv = sum(cashflow / (1 + period_discount_rate)**(t + 1) for t, cashflow in enumerate(cashflows))
        return pv