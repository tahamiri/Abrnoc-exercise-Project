from __future__ import annotations

from database import Base
from sqlalchemy import Column , String , Integer , Float , Boolean , ForeignKey , DateTime , Table
from sqlalchemy.orm import relationship , Mapped , mapped_column
from typing import List

association_table = Table(
    "association_table",
    Base.metadata,
    Column("left_id", ForeignKey("customers.id")),
    Column("right_id", ForeignKey("subscriptions.id")),
)







class Customer(Base):
    __tablename__ = "customers"
    
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username = Column(String, unique=True)
    credit = Column(Float)
    invoice: Mapped[List["Invoice"]] = relationship(back_populates="customer")
    subscription: Mapped[List[Subscription]] = relationship(
        secondary=association_table, back_populates="customer"
    )

class Subscription(Base):
    __tablename__ = "subscriptions"


    name = Column(String, unique=True)
    price = Column(Float)
    id: Mapped[int] = mapped_column(primary_key=True)
    customer: Mapped[List[Customer]] = relationship(
        secondary=association_table, back_populates="subscription"
    )

class Invoice(Base):
    __tablename__ = "invoice"
    
    
    price = Column(Float)
    start_date = Column(String)
    id: Mapped[int] = mapped_column(primary_key=True)
    end_date = Column(String)
    customer_id1: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    customer: Mapped["Customer"] = relationship(back_populates="invoice")

