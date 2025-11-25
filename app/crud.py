# app/crud.py

from sqlalchemy.orm import Session
from sqlalchemy import desc
from . import models, schemas, deps

# =================================================================
# CRUD (Create, Read, Update, Delete) 로직 모음
# 라우터(Router)에서 데이터베이스 작업이 필요할 때 이 함수들을 호출합니다.
# =================================================================


# -----------------------------------------------------------------
# 1. 사용자(User) 관련 DB 작업
# -----------------------------------------------------------------

def get_user_by_email(db: Session, email: str):
    """
    이메일로 사용자 정보를 조회합니다. (로그인, 회원가입 중복검사 시 사용)
    """
    return db.query(models.User).filter(models.User.email == email).first()

def get_user(db: Session, user_id: str):
    """
    User ID(UUID)로 사용자 정보를 조회합니다.
    """
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    """
    새로운 사용자를 DB에 생성합니다.

    [주요 로직]
    1. 입력받은 비밀번호를 deps.get_password_hash()로 암호화합니다.
    2. 기본 매너온도는 모델 디폴트값(36.5)을 따릅니다.
    """
    # 비밀번호 암호화 (보안 필수)
    hashed_pw = deps.get_password_hash(user.password)

    db_user = models.User(
        email=user.email,
        password_hash=hashed_pw, # 암호화된 문자열 저장
        name=user.name,
        nickname=user.nickname,
        region_id="서울" # 현재는 서울로 고정 (추후 확장 가능)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user) # DB에서 생성된 ID, Default값 등을 새로고침해서 가져옴
    return db_user


# -----------------------------------------------------------------
# 2. 상품(Item) 관련 DB 작업
# -----------------------------------------------------------------

def create_item(db: Session, item: schemas.ItemCreate, user_id: str):
    """
    새로운 판매 게시글을 생성합니다.
    seller_id에는 현재 로그인한 사용자의 ID가 들어갑니다.
    """
    db_item = models.Item(
        seller_id=user_id,
        title=item.title,
        content=item.content,
        price=item.price,
        category=item.category,
        region_id=item.region_id,
        image_urls=item.image_urls, # JSON 리스트 형태로 저장됨
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session, skip: int = 0, limit: int = 10, region_id: str = None):
    """
    상품 목록을 조회합니다. (필터링 + 페이지네이션 + 정렬)

    Returns:
        (items, total): 검색된 상품 리스트와 전체 개수를 튜플로 반환
    """
    query = db.query(models.Item)

    # 지역 필터링 (필수)
    if region_id:
        query = query.filter(models.Item.region_id == region_id)

    # 전체 개수 카운트 (페이지네이션 계산용)
    total = query.count()

    # 최신순 정렬 (created_at 내림차순) -> 페이지 자르기 (offset/limit)
    items = query.order_by(desc(models.Item.created_at)).offset(skip).limit(limit).all()

    return items, total

def get_item(db: Session, item_id: str):
    """
    특정 상품의 상세 정보를 조회합니다.
    """
    return db.query(models.Item).filter(models.Item.item_id == item_id).first()

def update_item_status(db: Session, item_id: str, status: str):
    """
    상품의 판매 상태를 변경합니다. (SELLING -> RESERVED -> SOLD)
    """
    item = get_item(db, item_id)
    if item:
        item.status = status
        db.commit()
        db.refresh(item)
    return item

def increase_view_count(db: Session, item_id: str):
    """
    상품 조회수를 1 증가시킵니다.
    (상세 페이지 API가 호출될 때 실행됨)
    """
    item = get_item(db, item_id)
    if item:
        item.views += 1
        db.commit() # 별도 refresh 불필요


# -----------------------------------------------------------------
# 3. 후기(Review) 및 매너온도 관련 DB 작업
# -----------------------------------------------------------------

def create_review(db: Session, review: schemas.ReviewCreate, reviewer_id: str, target_user_id: str):
    """
    후기를 생성하고, 대상 사용자의 매너온도를 업데이트합니다.

    [비즈니스 로직]
    - 긍정 평가(is_positive=True): 매너온도 +0.1
    - 부정 평가(is_positive=False): 매너온도 -0.1
    """
    # 1. 리뷰 기록 저장
    db_review = models.Review(
        reviewer_id=reviewer_id,
        target_user_id=target_user_id,
        item_id=review.item_id,
        is_positive=review.is_positive,
        evaluation_points=review.evaluation_points
    )
    db.add(db_review)

    # 2. 상대방 매너온도 업데이트
    target_user = get_user(db, target_user_id)
    if review.is_positive:
        target_user.manner_temperature += 0.1
    else:
        target_user.manner_temperature -= 0.1

    # 부동소수점 오차 방지를 위해 소수점 첫째자리에서 반올림
    target_user.manner_temperature = round(target_user.manner_temperature, 1)

    db.commit()
    db.refresh(db_review)

    # 생성된 리뷰와 업데이트된 온도를 함께 반환
    return db_review, target_user.manner_temperature

def get_reviews_stats(db: Session, user_id: str):
    """
    특정 사용자가 받은 긍정적인 평가 포인트들을 집계합니다.
    예: {"친절해요": 5, "시간약속을 잘 지켜요": 3}
    """
    # 사용자가 받은 모든 리뷰 조회
    reviews = db.query(models.Review).filter(models.Review.target_user_id == user_id).all()

    stats = {}
    for review in reviews:
        # 긍정적인 리뷰이고, 평가 항목(리스트)이 있는 경우만 집계
        if review.is_positive and review.evaluation_points:
            for point in review.evaluation_points:
                # 기존 값에 +1, 없으면 0에서 시작해서 +1
                stats[point] = stats.get(point, 0) + 1

    return stats