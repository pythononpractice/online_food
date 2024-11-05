from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base


class Review(Base):
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
