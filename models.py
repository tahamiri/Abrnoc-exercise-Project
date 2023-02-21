from database import Base
from sqlalchemy import Column , String , Integer , Float , Boolean , ForeignKey , DateTime
from sqlalchemy.orm import relationship

class Customer(Base):
    __tablename__ = "customers"
    
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    credit = Column(Float)
    subscription_id = Column("subscription_id", Integer, ForeignKey("subscriptions.id"))
    subscription = relationship("Subscription", backref="customers")
    invoice = relationship("Invoice", backref="customers")


class Subscription(Base):
    __tablename__ = "subscriptions"


    name = Column(String, unique=True)
    price = Column(Float)
    active = Column(Boolean)
    id = Column("id", Integer, primary_key=True)
    customer_id = Column("customer_id", Integer, ForeignKey("customers.id"))
    customer = relationship("Customer", backref="subscriptoins")


class Invoice(Base):
    __tablename__ = "invoice"
    
    
    price = Column(Float)
    start_date = Column(DateTime)
    id = Column("id", Integer, primary_key=True)
    end_date = Column(DateTime)
    customer_id = Column("customer_id", Integer, ForeignKey("customers.id"))

