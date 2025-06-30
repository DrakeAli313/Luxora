from pydantic import BaseModel, Field

class MortgageInput(BaseModel):
    purchase_price: float = Field(..., gt=0)
    down_payment: float = Field(default=0, ge=0)
    down_payment_percent: float = Field(default=None, ge=0, le=100)
    loan_term_years: int = Field(..., description="Allowed: 15, 20, 30")
    interest_rate: float = Field(default=6.63, gt=0)