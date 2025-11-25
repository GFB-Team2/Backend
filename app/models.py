from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, JSON, Enum as SAEnum
from sqlalchemy.sql import func
from .database import Base
import uuid
import enum

class ItemStatus(str, enum.Enum):
    SELLING = "SELLING"
    RESERVED = "RESERVED"
    SOLD = "SOLD"

class User(Base):
    __tablename__ = "users"
    user_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    name = Column(String)
    nickname = Column(String)
    manner_temperature = Column(Float, default=36.5)
    region_id = Column(String, default="서울")

class Item(Base):
    __tablename__ = "items"
    item_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    seller_id = Column(String, ForeignKey("users.user_id"))
    title = Column(String)
    content = Column(String)
    price = Column(Integer)
    category = Column(String)
    status = Column(SAEnum(ItemStatus), default=ItemStatus.SELLING)
    region_id = Column(String)
    image_urls = Column(JSON, default=[])
    views = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Review(Base):
    __tablename__ = "reviews"
    review_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    reviewer_id = Column(String, ForeignKey("users.user_id"))
    target_user_id = Column(String, ForeignKey("users.user_id"))
    item_id = Column(String, ForeignKey("items.item_id"))
    is_positive = Column(Boolean, default=True)
    evaluation_points = Column(JSON, default=[])
    created_at = Column(DateTime(timezone=True), server_default=func.now())