from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum

class ItemStatus(str, Enum):
    SELLING = "SELLING"
    RESERVED = "RESERVED"
    SOLD = "SOLD"

# User
class UserCreate(BaseModel):
    email: str
    password: str
    name: str
    nickname: str

class LoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    user_id: str
    email: str
    nickname: str
    name: str
    manner_temperature: float
    region_name: str = "당근동"
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# Item
class ItemCreate(BaseModel):
    title: str
    content: str
    price: int
    category: str
    region_id: str
    image_urls: List[str] = []

class ItemStatusUpdate(BaseModel):
    status: ItemStatus

class SellerInfo(BaseModel):
    user_id: str
    nickname: str
    manner_temperature: float
    class Config:
        from_attributes = True

class ItemDetailResponse(BaseModel):
    item_id: str
    title: str
    content: str
    price: int
    seller: SellerInfo
    region_name: str = "당근동"
    created_at: datetime
    views: int
    image_urls: List[str]
    status: ItemStatus
    class Config:
        from_attributes = True

class ItemListResponse(BaseModel):
    items: List[dict]
    total_count: int

# Review
class ReviewCreate(BaseModel):
    item_id: str
    is_positive: bool
    evaluation_points: List[str]

class ReviewResponse(BaseModel):
    review_id: str
    target_user_id: str
    new_temperature: float

class MannerStatsResponse(BaseModel):
    manner_temperature: float
    positive_reviews: Dict[str, int]