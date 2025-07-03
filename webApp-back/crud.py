from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from .schemas import PersonCreate
from .models import PersonDB
from .database import get_db

#Person functions

async def add_person(item: PersonCreate, db: Session = Depends(get_db)):
    db_item = PersonDB(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

async def read_person(item_id : int, db: Session = Depends(get_db)):
    db_item = db.query(PersonDB).filter(PersonDB.id == item_id).first()
    return db_item

def read_all_person(db: Session):
    return db.query(PersonDB).all()  

async def update_person(item_id : int,item: PersonCreate ,db: Session = Depends(get_db)):
    db_item = db.query(PersonDB).filter(PersonDB.id == item_id).first()
    if db_item == None:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.model_dump().items():
        setattr(db_item, key , value)
    db.commit()
    db.refresh(db_item)
    return db_item

async def delete_person(item_id : int ,db: Session = Depends(get_db)):
    db_item = db.query(PersonDB).filter(PersonDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return { "message": "Item Deleted" }

def print_PersonDB(db: Session = Depends(get_db)):
    people = db.query(PersonDB).all()
    for person in people:
        print(person.__dict__)

