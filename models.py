from database import Base
from sqlalchemy import Column , String , Integer , Float


class Customer(Base):
    __tablename__ = "customers"
    
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    credit = Column(Float)


