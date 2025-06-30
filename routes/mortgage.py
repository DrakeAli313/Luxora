from fastapi import APIRouter, HTTPException
from schemas.mortgage import MortgageInput

router = APIRouter()


@router.post("/mortgage/calculate")
def calculate_mortgage(data: MortgageInput):
    purchase_price = data.purchase_price

    # Step 1: Determine down payment amount
    if data.down_payment_percent is not None:
        down_payment_amount = (data.down_payment_percent / 100.0) * purchase_price
        down_payment_percent = data.down_payment_percent
    elif data.down_payment is not None:
        down_payment_amount = data.down_payment
        down_payment_percent = (down_payment_amount / purchase_price) * 100
    else:
        raise HTTPException(status_code=400, detail="Provide either down_payment or down_payment_percent.")

    # Step 2: Validate loan term
    if data.loan_term_years not in [15, 20, 30]:
        raise HTTPException(status_code=400, detail="Loan term must be 15, 20, or 30 years.")

    loan_amount = purchase_price - down_payment_amount
    annual_rate = data.interest_rate / 100
    monthly_rate = annual_rate / 12
    total_payments = data.loan_term_years * 12

    # Step 3: Calculate monthly mortgage payment
    monthly_payment = (
        loan_amount * monthly_rate * (1 + monthly_rate) ** total_payments
    ) / ((1 + monthly_rate) ** total_payments - 1)

    return {
        "purchase_price": round(purchase_price, 2),
        "down_payment_amount": round(down_payment_amount, 2),
        "down_payment_percent": round(down_payment_percent, 2),
        "estimated_monthly_payment": round(monthly_payment, 2),
        "message": (
            f"💸 With a down payment of ${round(down_payment_amount, 2)} "
            f"({round(down_payment_percent, 2)}%), your estimated monthly payment is "
            f"${round(monthly_payment, 2)}. Let's make homeownership a reality! 🏠"
        )
    }
