from sqlalchemy import Column, Integer, String
from app.core.db import Base


class Restaurant(Base):
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    location = Column(String, nullable=True)
