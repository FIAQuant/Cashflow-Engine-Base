
# Cashflow Calculation Engine

A Python-based tool for calculating cashflows, yields, and present values for bonds and related assets. This engine supports corporate bonds, callable bonds, and gilts, including features like inflation-linked cashflows and stress testing scenarios.

---

## **Features**

- **Corporate Bonds**:
  - Calculates Yield to Maturity (YTM) and present value (PV).
  - Handles fixed-rate and inflation-linked bonds.
  - Supports dynamic coupon adjustments via haircut (in bps).

- **Callable Bonds**:
  - Computes Yield to Worst (YTW) and identifies worst-case cashflows.
  - Evaluates all possible call scenarios based on user inputs.

- **Gilts**:
  - Supports fixed-rate and inflation-linked gilts.
  - Generates cashflows adjusted for inflation curves.

- **Stress Testing**:
  - Adjusts rates (RFR and spreads) and calculates stressed PVs for different scenarios.
  - Supports coupon rate haircuts for stress scenarios.

---

## **Installation**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/username/my-cashflow-engine.git
   cd my-cashflow-engine
   ```

2. **Set Up Environment**:
   - Install required Python packages:
     ```bash
     pip install numpy numpy-financial
     ```

3. **Run the Application**:
   - Execute the `main.py` script:
     ```bash
     python main.py
     ```

---

## **Usage**

### **Corporate Bond Example**
- Base and stressed PV and YTM:
  ```python
  corp_calc = CorporateBondCalculator()
  cashflows = corp_calc.generate_cashflows(
      face_value=1000,
      coupon_rate=0.05,
      maturity=5,
      payment_frequency=1
  )
  ytm = corp_calc.calculate_yield_to_maturity(cashflows, market_price=950)
  ```

### **Callable Bond Example**
- Yield to Worst and worst-case cashflows:
  ```python
  call_calc = CallableBondCalculator()
  ytw, worst_cashflows = call_calc.calculate_yield_to_worst(
      face_value=1000,
      coupon_rate=0.05,
      call_dates=[5, 10],
      call_prices=[1020, 1010],
      maturity=10,
      market_price=950
  )
  ```

### **Gilt Example**
- Inflation-linked gilt PV:
  ```python
  gilt_calc = GiltCalculator()
  gilt_cashflows = gilt_calc.generate_cashflows(
      face_value=1000,
      coupon_rate=0.05,
      maturity=5,
      gilt_type="inflation-linked",
      inflation_curve=[1.01, 1.02, 1.03, 1.04, 1.05]
  )
  ```

---

## **Project Structure**
```
my-cashflow-engine/
├── calculators/
│   ├── corporate_bond_calculator.py
│   ├── callable_bond_calculator.py
│   ├── gilt_calculator.py
├── main.py
├── signature.py
├── README.md
├── .gitignore
```

---

## **Contributing**
Contributions are welcome! Please fork the repository and submit a pull request.

---

## **License**
This project is licensed under the MIT License.

---

## **Contact**
For support or inquiries, please contact **Azim Patel**.
