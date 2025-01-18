def apply_stress_to_rate(rfr, spread, stress_rfr_bps=0, stress_spread_bps=0):
    """
    Apply stress to the risk-free rate (RFR) or spread by given bps.
    """
    stressed_rfr = rfr + stress_rfr_bps / 10000
    stressed_spread = spread + stress_spread_bps / 10000
    return stressed_rfr + stressed_spread