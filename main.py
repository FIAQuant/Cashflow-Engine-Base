from calculators.corporate_bond_calculator import CorporateBondCalculator
from calculators.callable_bond_calculator import CallableBondCalculator
from calculators.gilt_calculator import GiltCalculator
from metadata.signature import __author__, __version__

# Base data
face_value = 1000
coupon_rate = 0.05
maturity = 5
payment_frequency = 1
market_price = 950
rfr = 0.03  # 3% RFR
spread = 0.02  # 2% spread

# Stress parameters
stress_rfr_bps = 50  # +50 bps to RFR
stress_spread_bps = 100  # +100 bps to spread
haircut_bps = 25  # Haircut to coupon rate (-0.25%)

# Corporate Bond Example
corp_calc = CorporateBondCalculator()

# Base Scenario (Corporate Bond)
corp_cashflows_base = corp_calc.generate_cashflows(
    face_value=face_value,
    coupon_rate=coupon_rate,
    maturity=maturity,
    payment_frequency=payment_frequency,
    bond_type="fixed",
    haircut_bps=0
)
corp_ytm_base = corp_calc.calculate_yield_to_maturity(
    corp_cashflows_base, market_price, payment_frequency
)

# Stressed Scenario with Haircut (Corporate Bond)
corp_cashflows_stressed = corp_calc.generate_cashflows(
    face_value=face_value,
    coupon_rate=coupon_rate,
    maturity=maturity,
    payment_frequency=payment_frequency,
    bond_type="fixed",
    haircut_bps=haircut_bps
)
corp_ytm_stressed = corp_calc.calculate_yield_to_maturity(
    corp_cashflows_stressed, market_price, payment_frequency
)

# Callable Bond Example
call_calc = CallableBondCalculator()
call_dates = [5, 10]
call_prices = [1020, 1010]

# Base Scenario (Callable Bond)
ytw_base, callable_cashflows_base = call_calc.calculate_yield_to_worst(
    face_value=face_value,
    coupon_rate=coupon_rate,
    call_dates=call_dates,
    call_prices=call_prices,
    maturity=maturity,
    market_price=market_price,
    payment_frequency=payment_frequency,
    haircut_bps=0
)

# Stressed Scenario with Haircut (Callable Bond)
ytw_stressed, callable_cashflows_stressed = call_calc.calculate_yield_to_worst(
    face_value=face_value,
    coupon_rate=coupon_rate,
    call_dates=call_dates,
    call_prices=call_prices,
    maturity=maturity,
    market_price=market_price,
    payment_frequency=payment_frequency,
    haircut_bps=haircut_bps
)

# Gilt Example
gilt_calc = GiltCalculator()
inflation_curve = [1.01, 1.02, 1.03, 1.04, 1.05]  # Example inflation factors

# Base Scenario (Gilt)
gilt_cashflows_base = gilt_calc.generate_cashflows(
    face_value=face_value,
    coupon_rate=coupon_rate,
    maturity=maturity,
    payment_frequency=payment_frequency,
    gilt_type="inflation-linked",
    inflation_curve=inflation_curve,
    haircut_bps=0
)
gilt_ytm_base = gilt_calc.calculate_yield_to_maturity(
    gilt_cashflows_base, market_price, payment_frequency
)

# Stressed Scenario with Haircut (Gilt)
gilt_cashflows_stressed = gilt_calc.generate_cashflows(
    face_value=face_value,
    coupon_rate=coupon_rate,
    maturity=maturity,
    payment_frequency=payment_frequency,
    gilt_type="inflation-linked",
    inflation_curve=inflation_curve,
    haircut_bps=haircut_bps
)
gilt_ytm_stressed = gilt_calc.calculate_yield_to_maturity(
    gilt_cashflows_stressed, market_price, payment_frequency
)

# Output Results
print("Corporate Bond Results:")
print(f"  Base YTM: {corp_ytm_base:.2f}%")
print(f"  Base Cashflows: {corp_cashflows_base}")
print(f"  Stressed YTM (with Haircut): {corp_ytm_stressed:.2f}%")
print(f"  Stressed Cashflows: {corp_cashflows_stressed}")

print("\nCallable Bond Results:")
print(f"  Base YTW: {ytw_base:.2f}%")
print(f"  Base Worst-Case Cashflows: {callable_cashflows_base}")
print(f"  Stressed YTW (with Haircut): {ytw_stressed:.2f}%")
print(f"  Stressed Worst-Case Cashflows: {callable_cashflows_stressed}")

print("\nGilt Results:")
print(f"  Base YTM: {gilt_ytm_base:.2f}%")
print(f"  Base Cashflows: {gilt_cashflows_base}")
print(f"  Stressed YTM (with Haircut): {gilt_ytm_stressed:.2f}%")
print(f"  Stressed Cashflows: {gilt_cashflows_stressed}")

# Print signature information
print("\n" + "-" * 50)
print(f"{'Run Complete':^50}")
print("-" * 50)
print(f"Version: {__version__}")
print(f"Support Contact: {__author__}")
print("-" * 50)