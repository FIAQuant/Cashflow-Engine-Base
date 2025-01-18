import numpy_financial as npf

class CallableBondCalculator:
    """
    A calculation engine for callable bonds, including calculation of
    worst-case cashflows and Yield to Worst (YTW).
    """

    def calculate_yield(self, cashflows, market_price, payment_frequency=1):
        """
        Calculate the yield for a given cashflow scenario.

        Parameters:
        - cashflows (list of floats): Cashflows for the scenario.
        - market_price (float): Current price of the bond.
        - payment_frequency (int): Number of payments per year (e.g., 1 for annual, 2 for semiannual).

        Returns:
        - float: Yield as a decimal.
        """
        return npf.irr([-market_price] + cashflows) * payment_frequency

    def calculate_yield_to_worst(self, face_value, coupon_rate, call_dates, call_prices, maturity, market_price, payment_frequency=1, haircut_bps=0):
        """
        Calculate the Yield to Worst (YTW) and corresponding worst-case cashflows.

        Parameters:
        - face_value (float): The bond's par value (e.g., 1000).
        - coupon_rate (float): Annual coupon rate as a decimal (e.g., 0.05 for 5%).
        - call_dates (list of ints): List of call dates in years (e.g., [5, 10]).
        - call_prices (list of floats): Call prices at each call date (e.g., [1020, 1010]).
        - maturity (int): Time to maturity in years (e.g., 10).
        - market_price (float): Current price of the bond (e.g., 950).
        - payment_frequency (int): Number of coupon payments per year (e.g., 1 for annual, 2 for semiannual).
        - haircut_bps (float): Basis points adjustment to the coupon rate (e.g., 50 for -0.5%).

        Returns:
        - tuple: (YTW, worst-case cashflows)
        """
        # Adjust coupon rate based on the haircut
        haircut_decimal = haircut_bps / 10000
        adjusted_coupon_rate = coupon_rate * (1 - haircut_decimal)
        coupon_payment = face_value * adjusted_coupon_rate / payment_frequency
        periods = maturity * payment_frequency

        # Generate all cashflow scenarios
        cashflow_scenarios = []
        for call_date, call_price in zip(call_dates, call_prices):
            call_periods = call_date * payment_frequency
            cashflows = [coupon_payment] * (call_periods - 1) + [coupon_payment + call_price]
            cashflow_scenarios.append(cashflows)

        # Add the maturity scenario
        maturity_cashflows = [coupon_payment] * (periods - 1) + [coupon_payment + face_value]
        cashflow_scenarios.append(maturity_cashflows)

        # Calculate yield for each scenario and find the worst-case scenario
        yields_and_cashflows = [
            (self.calculate_yield(cashflows, market_price, payment_frequency), cashflows)
            for cashflows in cashflow_scenarios
        ]
        worst_yield, worst_cashflows = min(yields_and_cashflows, key=lambda x: x[0])

        return worst_yield * 100, worst_cashflows