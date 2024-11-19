from sqlalchemy import Column, Integer, String
from app.database import Base

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    front = Column(String, index=True)
    back = Column(String)  
