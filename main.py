from fastapi import FastAPI , Path , Query , status , HTTPException , Depends
from typing import Optional , Union
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine , SessionLocal
import schemas , models
import threading
from datetime import datetime


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
x = 0

def invoice(subscription_id2:int,customer_id2:int, db1: Session):
    timer = threading.Timer(600, invoice, args=(subscription_id2,customer_id2,db1))
    timer.start()
    
    global x
    if x == 0:
        now = datetime.now()
        now1 = f"{now.year}/{now.month}/{now.day} {now.hour}:{now.minute}:{now.second}"
        now2 = f"{now.year}/{now.month}/{now.day} {now.hour}:{now.minute+10}:{now.second}"
        sub = db1.query(models.Subscription).filter(models.Subscription.id==subscription_id2).first()
        pri = sub.price
        inv = models.Invoice(price=pri, start_date=now1 , end_date=now2 , customer_id1=customer_id2)
        db1.add(inv)
        db1.commit()
        cus = db1.query(models.Customer).filter(models.Customer.id==customer_id2).first()
        inv1 = db1.query(models.Invoice).filter(models.Invoice.start_date==now1).first()
        cus.invoice.append(inv1)
        cus.credit = cus.credit - inv.price
        db1.commit()
    else:
        timer.cancel()


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


@app.post("/subscriptions/", response_model=schemas.Subscription)
def create_subscription(subscription:schemas.SubscriptionBase, db: Session = Depends(get_db)):
    db_subscription = db.query(models.Subscription).filter(models.Subscription.name==subscription.name).first()
    if db_subscription:
        raise HTTPException(status_code=400, detail="subscription already exists")
    subscription = models.Subscription(name=subscription.name, price=subscription.price)
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription


@app.get("/subscriptions/{subscription_id}", response_model=schemas.Subscription)
def read_subscription(subscription_id:int, db: Session = Depends(get_db)):
    db_sub = db.query(models.Subscription).filter(models.Subscription.id==subscription_id).first()
    if db_sub is None:
        raise HTTPException(status_code=404, detail="subscription not found")
    return db_sub



@app.get("/addsub/{subscription_id1}/customer/{customer_id1}", response_model=schemas.Customer)
def add_sub(subscription_id1:int,customer_id1:int, db: Session = Depends(get_db), db1: Session = Depends(get_db)):
    #global subscription_id2 , customer_id2
    #subscription_id2 = subscription_id1
    #customer_id2 = customer_id1
    db_sub = db.query(models.Subscription).filter(models.Subscription.id==subscription_id1).first()
    if db_sub is None:
        raise HTTPException(status_code=404, detail="subscription not found")    
    db_cust = db.query(models.Customer).filter(models.Customer.id==customer_id1).first()
    if db_cust is None:
        raise HTTPException(status_code=404, detail="customer not found")
    db_cust.subscription.append(db_sub)
    invoice(subscription_id1,customer_id1, db1)
    db.commit()
    
    return db_cust


@app.get("/delsub/{subscription_id}/customer/{customer_id}", response_model=schemas.Customer)
def add_sub(subscription_id:int,customer_id:int, db: Session = Depends(get_db)):
    db_sub = db.query(models.Subscription).filter(models.Subscription.id==subscription_id).first()
    if db_sub is None:
        raise HTTPException(status_code=404, detail="subscription not found")    
    db_cust = db.query(models.Customer).filter(models.Customer.id==customer_id).first()
    if db_cust is None:
        raise HTTPException(status_code=404, detail="customer not found")
    
    try:
        db_cust.subscription.remove(db_sub)
        global x
        x = 1
        db.commit()
        return db_cust
    except ValueError:
        return db_cust

    






