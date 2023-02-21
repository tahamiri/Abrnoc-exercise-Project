from pydantic import BaseModel


class CustomerBase(BaseModel):
    username: str
    credit: float


class Customer(CustomerBase):
    id: int
    subscription: list
    invoice: list
    class Config:
        orm_mode = True


class SubscriptionBase(BaseModel):
    name: str
    price: float

class Subscription(SubscriptionBase):
    id: int
    customer: list
    class Config:
        orm_mode = True


class InvoiceBase(BaseModel):
    price: float
    start_date: str
    end_date: str

class Invoice(InvoiceBase):
    id: int
    class Config:
        orm_mode = True




