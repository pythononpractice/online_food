from sqlalchemy import Column, String, Boolean
from app.core.db import Base


class User(Base):
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
