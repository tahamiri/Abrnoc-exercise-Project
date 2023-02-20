from fastapi import FastAPI , Path , Query , status , HTTPException , Depends
from typing import Optional , Union
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine , SessionLocal
import schemas , models


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/customers/", response_model=schemas.Customer)
def create_customer(customer:schemas.CustomerBase, db: Session = Depends(get_db)):
    db_customer = db.query(models.Customer).filter(models.Customer.username==customer.username).first()
    if db_customer:
        raise HTTPException(status_code=400, detail="username already exists")
    customer = models.Customer(username=customer.username, credit=customer.credit)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer



@app.get("/customers/{customer_id}", response_model=schemas.Customer)
def read_customer(customer_id:int, db: Session = Depends(get_db)):
    db_user = db.query(models.Customer).filter(models.Customer.id==customer_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="customer not found")
    return db_user















