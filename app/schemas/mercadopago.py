from pydantic import BaseModel


class CheckoutItem(BaseModel):
    title: str
    quantity: int
    unit_price: float
    description: str | None = None


class CheckoutRequest(BaseModel):
    items: list[CheckoutItem]
    success_url: str
    failure_url: str
    pending_url: str