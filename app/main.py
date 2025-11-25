from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .database import engine, Base
from .routers import auth, users, items
import os

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

# 이미지 폴더 없으면 자동 생성
if not os.path.exists("images"):
    os.makedirs("images")

app = FastAPI()

# CORS 설정 (테스트용 모두 허용)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 이미지 파일 정적 경로 설정 (http://.../images/파일.jpg)
app.mount("/images", StaticFiles(directory="images"), name="images")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(items.router)

@app.get("/")
def root():
    return {"message": "Carrot Market API is Running!"}