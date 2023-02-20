from pydantic import BaseModel


class CustomerBase(BaseModel):
    username: str
    credit: float


class Customer(CustomerBase):
    id: int
    class Config:
        orm_mode = True
