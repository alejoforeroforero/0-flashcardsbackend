from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import app.models as models
from app.database import engine, SessionLocal


app = FastAPI(root_path="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8081"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Card(BaseModel):
    front: str = Field(min_length=1)
    back: str = Field(min_length=1)

@app.get('/')
def read_cards(db: Session = Depends(get_db)):
    return db.query(models.Card).all()

@app.post('/')
def create_card(card: Card, db: Session = Depends(get_db)):
    car_model = models.Card()
    car_model.front = card.front
    car_model.back = card.back

    db.add(car_model)
    db.commit()
    return card

@app.put('/{id}')
def update_info(card_id: int, card: Card, db: Session = Depends(get_db)):

    car_model = db.query(models.Card).filter(models.Card.id == card_id).first()

    if car_model is None:
        raise HTTPException(
            status_code=400,
            detail=f"algo pasa"
        )
    car_model.front = card.front
    car_model.back = card.back


    db.add(car_model)
    db.commit()
    return card

@app.delete('/{id}')
def delete_info(card_id: int, db: Session = Depends(get_db)):
    card_model = db.query(models.Card).filter(models.Card.id == card_id).first()

    if card_model is None:
        raise HTTPException(
            status_code=400,
            detail=f"algo paso"
        )

    db.query(models.Card).filter(models.Card.id == card_id).delete()
    db.commit()
