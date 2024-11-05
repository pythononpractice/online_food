from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app.core.db import Base
import enum
from datetime import datetime


class OrderStatus(enum.Enum):
    pending = "pending"
    in_process = "in_process"
    delivered = "delivered"
    canceled = "canceled"


class Order(Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    dish_id = Column(Integer, ForeignKey('dish.id'))
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)
    created_at = Column(DateTime, default=datetime.utcnow)
