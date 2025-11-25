# app/routers/items.py

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
import shutil
from .. import schemas, database, crud, deps, models

# =================================================================
# 상품(Item) 관련 API 라우터
# 상품 등록, 조회, 이미지 업로드, 상태 변경 기능을 담당합니다.
# Prefix: /api/v1/items
# =================================================================
router = APIRouter(prefix="/api/v1/items", tags=["Items"])

# -----------------------------------------------------------------
# 0. 이미지 업로드 API (POST /api/v1/items/upload)
# -----------------------------------------------------------------
@router.post("/upload")
def upload_file(file: UploadFile = File(...)):
    """
    [이미지 업로드]
    프론트엔드에서 이미지 파일을 받아 서버의 'images' 폴더에 저장합니다.

    Args:
        file (UploadFile): 업로드할 이미지 파일

    Returns:
        dict: 저장된 이미지에 접근할 수 있는 URL 반환

    Note:
        실제 상용 서비스(Production)에서는 서버 로컬 디스크 대신
        AWS S3 같은 클라우드 스토리지를 사용하는 것이 좋습니다.
    """

    # 1. 저장할 파일 경로 설정 (images 폴더 내 파일명)
    # 주의: 파일명이 겹치지 않도록 UUID 등을 붙이는 것이 안전하지만, 현재는 원본명 사용
    file_location = f"images/{file.filename}"

    # 2. 서버 로컬 디스크에 파일 저장 (wb+ 모드: 바이너리 쓰기)
    with open(file_location, "wb+") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 3. 외부에서 접근 가능한 URL 생성하여 반환
    # app/main.py에서 StaticFiles로 마운트한 경로와 일치해야 함
    return {"url": f"http://localhost:8000/images/{file.filename}"}


# -----------------------------------------------------------------
# 1. 게시글 등록 API (POST /api/v1/items)
# -----------------------------------------------------------------
@router.post("", response_model=dict)
def create_item(
    item: schemas.ItemCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    [상품 등록]
    로그인한 사용자가 새로운 중고 거래 게시글을 등록합니다.

    Args:
        item (ItemCreate): 제목, 가격, 내용, 카테고리, 이미지 URL 리스트 등
        current_user (User): 현재 로그인한 사용자 (Dependency로 주입)

    Returns:
        dict: 생성된 상품의 ID, 제목, 생성일시
    """

    # CRUD 함수 호출 시 로그인한 유저의 ID(user_id)를 함께 전달하여 소유자 지정
    new_item = crud.create_item(db=db, item=item, user_id=current_user.user_id)

    return {
        "item_id": new_item.item_id,
        "title": new_item.title,
        "created_at": new_item.created_at
    }


# -----------------------------------------------------------------
# 2. 상품 목록 조회 API (GET /api/v1/items)
# -----------------------------------------------------------------
@router.get("", response_model=schemas.ItemListResponse)
def read_items(
    region_id: str = Query(..., description="조회할 지역 ID (필수)"),
    category: Optional[str] = Query(None, description="카테고리 필터 (선택)"),
    page: int = Query(1, description="페이지 번호 (기본 1)"),
    limit: int = Query(10, description="페이지당 게시글 수 (기본 10)"),
    db: Session = Depends(database.get_db)
):
    """
    [상품 목록 조회]
    특정 지역의 상품 목록을 최신순으로 조회합니다. (페이지네이션 적용)

    Args:
        region_id (str): 필수 필터. 사용자의 지역 또는 선택한 지역
        page (int): 페이지 번호
        limit (int): 가져올 개수

    Returns:
        ItemListResponse: 상품 요약 정보 리스트와 전체 개수(total_count)
    """

    # 페이지네이션 계산 (SQL OFFSET)
    skip = (page - 1) * limit

    # DB에서 데이터 조회
    items, total = crud.get_items(db, skip=skip, limit=limit, region_id=region_id)

    # 응답 데이터 구성 (리스트 목록용 요약 정보)
    item_list = []
    for item in items:
        item_list.append({
            "item_id": item.item_id,
            "title": item.title,
            "price": item.price,
            "region_name": "당근동", # 추후 Region 테이블 조인 필요 (현재는 고정값)
            "created_at": item.created_at,
            # Enum 비교: DB의 상태가 SOLD(판매완료)인지 확인
            "is_sold": item.status == models.ItemStatus.SOLD,
            # 목록에서는 대표 이미지 1장만 보여줌 (없으면 None)
            "main_image_url": item.image_urls[0] if item.image_urls else None
        })

    return {"items": item_list, "total_count": total}


# -----------------------------------------------------------------
# 3. 상품 상세 조회 API (GET /api/v1/items/{item_id})
# -----------------------------------------------------------------
@router.get("/{item_id}", response_model=schemas.ItemDetailResponse)
def read_item_detail(item_id: str, db: Session = Depends(database.get_db)):
    """
    [상품 상세 조회]
    상품의 상세 정보를 조회하고 조회수(view)를 1 증가시킵니다.

    Args:
        item_id (str): 조회할 상품의 UUID

    Raises:
        404 Not Found: 해당 ID의 상품이 없을 경우
    """

    # 1. 조회수 증가 로직 (비즈니스 요구사항)
    crud.increase_view_count(db, item_id)

    # 2. 상품 정보 가져오기
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # 3. 판매자 정보 가져오기 (상세 페이지에 판매자 닉네임, 매너온도 표시용)
    seller = crud.get_user(db, item.seller_id)

    # 4. 응답 반환 (Pydantic 스키마에 맞춰 매핑됨)
    return {
        "item_id": item.item_id,
        "title": item.title,
        "content": item.content,
        "price": item.price,
        "seller": seller, # seller 객체를 통째로 넘기면 SellerInfo 스키마가 필터링함
        "region_name": "당근동",
        "created_at": item.created_at,
        "views": item.views,
        "image_urls": item.image_urls,
        "status": item.status
    }


# -----------------------------------------------------------------
# 4. 상품 상태 변경 API (PATCH /api/v1/items/{item_id}/status)
# -----------------------------------------------------------------
@router.patch("/{item_id}/status")
def update_status(
    item_id: str,
    status_update: schemas.ItemStatusUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    [상품 상태 변경]
    판매 중(SELLING) <-> 예약 중(RESERVED) <-> 판매 완료(SOLD) 상태를 변경합니다.
    작성자(Seller) 본인만 변경 가능합니다.

    Args:
        status_update (ItemStatusUpdate): 변경할 상태값 (Enum)
        current_user (User): 현재 로그인한 사용자

    Raises:
        403 Forbidden: 작성자가 아닌 사람이 수정을 시도할 경우
        404 Not Found: 상품이 없을 경우
    """

    # 1. 상품 존재 확인
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # 2. 권한 체크: 현재 로그인한 사용자가 판매자인지 확인
    if item.seller_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized (작성자만 상태를 변경할 수 있습니다)")

    # 3. 상태 업데이트 실행
    crud.update_item_status(db, item_id, status_update.status)

    return {"message": "Status updated successfully"}