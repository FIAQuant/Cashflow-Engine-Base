from calculators.cashflow_calculator import CashflowCalculator
from utilities.stress_testing import apply_stress_to_rate
import numpy_financial as npf


class CorporateBondCalculator(CashflowCalculator):
    """
    Handles corporate bond-specific calculations, including fixed-rate,
    inflation-linked, and zero-coupon bonds.
    """

    def generate_cashflows(self, face_value, coupon_rate, maturity, payment_frequency=1, bond_type="fixed", inflation_curve=None, haircut_bps=0):
        """
        Generate cashflows for a corporate bond, supporting fixed-rate, inflation-linked, and zero-coupon bonds.

        Parameters:
        - face_value (float): The bond's par value (e.g., 1000).
        - coupon_rate (float): Annual coupon rate as a decimal (e.g., 0.05 for 5%). For zero-coupon bonds, set to 0.
        - maturity (int): Time to maturity in years (e.g., 10).
        - payment_frequency (int): Number of coupon payments per year (e.g., 1 for annual, 2 for semiannual).
        - bond_type (str): Type of bond - "fixed", "inflation-linked", or "zero-coupon".
        - inflation_curve (list of floats): Inflation adjustment factors for each year (optional, only used for "inflation-linked").
        - haircut_bps (float): Optional basis points adjustment to the coupon rate (e.g., 50 for -0.5%).

        Returns:
        - list: Cashflows for the bond over its lifetime.
        """
        if bond_type == "zero-coupon":
            # Zero-coupon bonds have no periodic payments; single cashflow at maturity
            return [face_value]

        # Adjust coupon rate based on the haircut
        haircut_decimal = haircut_bps / 10000
        adjusted_coupon_rate = coupon_rate * (1 - haircut_decimal)
        coupon_payment = face_value * adjusted_coupon_rate / payment_frequency
        periods = maturity * payment_frequency

        if bond_type == "inflation-linked":
            if not inflation_curve or len(inflation_curve) < periods:
                raise ValueError("Inflation curve must match the number of periods for inflation-linked bonds.")
            # Adjust coupon payments based on inflation factors
            cashflows = [
                coupon_payment * inflation_curve[i] for i in range(periods - 1)
            ]
            final_payment = (coupon_payment + face_value) * inflation_curve[-1]
            cashflows.append(final_payment)
        else:  # Default to "fixed" bond
            cashflows = [coupon_payment] * (periods - 1)
            cashflows.append(coupon_payment + face_value)

        return cashflows

    def calculate_yield_to_maturity(self, cashflows, market_price, payment_frequency=1):
        """
        Calculate the Yield to Maturity (YTM) for a corporate bond.

        Parameters:
        - cashflows (list of floats): List of cashflows for the bond.
        - market_price (float): Current market price of the bond.
        - payment_frequency (int): Number of coupon payments per year (e.g., 1 for annual, 2 for semiannual).

        Returns:
        - float: Yield to Maturity (YTM) as a percentage.
        """
        ytm = npf.irr([-market_price] + cashflows) * payment_frequency * 100
        return ytm

    def present_value_at_time_t(self, cashflows, discount_rate, payment_frequency=1, time_t=0, inflation_adjustment=None):
        """
        Calculate the present value (PV) of a corporate bond at a specific time `t`.

        Parameters:
        - cashflows (list of floats): List of cashflows for the bond.
        - discount_rate (float): Annual discount rate as a decimal (e.g., 0.04 for 4%).
        - payment_frequency (int): Number of coupon payments per year (e.g., 1 for annual, 2 for semiannual).
        - time_t (int): Time in years from which to calculate PV (default is 0).
        - inflation_adjustment (list of floats): Optional inflation factors to adjust remaining cashflows.

        Returns:
        - float: The present value (PV) of the bond.
        """
        period_discount_rate = discount_rate / payment_frequency
        remaining_cashflows = cashflows[time_t * payment_frequency:]

        if inflation_adjustment:
            remaining_cashflows = [
                cf * inflation_adjustment[i] for i, cf in enumerate(remaining_cashflows)
            ]

        pv = sum(cashflow / (1 + period_discount_rate)**(t + 1) for t, cashflow in enumerate(remaining_cashflows))
        return pv

    def calculate_stressed_pv(self, cashflows, rfr, spread, stress_rfr_bps=0, stress_spread_bps=0, payment_frequency=1):
        """
        Calculate the PV of the bond under stressed conditions.

        Parameters:
        - cashflows (list of floats): List of cashflows for the bond.
        - rfr (float): Base risk-free rate (RFR), as a decimal (e.g., 0.03 for 3%).
        - spread (float): Additional spread to apply, as a decimal (e.g., 0.01 for 1%).
        - stress_rfr_bps (float): Basis points to stress the RFR (e.g., 50 for +0.5%).
        - stress_spread_bps (float): Basis points to stress the spread (e.g., 20 for +0.2%).
        - payment_frequency (int): Number of payments per year (e.g., 1 for annual, 2 for semiannual).

        Returns:
        - float: The present value (PV) of the bond under stressed conditions.
        """
        stressed_rate = apply_stress_to_rate(rfr, spread, stress_rfr_bps, stress_spread_bps)
        return self.calculate_present_value(cashflows, stressed_rate, payment_frequency)