# app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, deps, database, crud

# =================================================================
# 사용자(User) 관련 API 라우터
# 내 정보 조회, 매너온도 평가(후기), 매너온도 조회 기능을 담당합니다.
# Prefix: /api/v1/users
# =================================================================
router = APIRouter(prefix="/api/v1/users", tags=["Users"])


# -----------------------------------------------------------------
# 1. 내 정보 조회 API (GET /api/v1/users/me)
# -----------------------------------------------------------------
@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(deps.get_current_user)):
    """
    [내 정보 조회]
    현재 로그인된 사용자(Access Token 소유자)의 프로필 정보를 반환합니다.

    Args:
        current_user (User): 헤더의 토큰으로 식별된 현재 사용자 (Dependency)

    Returns:
        UserResponse: 사용자 ID, 이메일, 닉네임, 매너온도, 지역 정보
    """
    # deps.get_current_user가 토큰 검증 및 DB 조회를 마친 user 객체를 줍니다.
    return current_user


# -----------------------------------------------------------------
# 2. 매너온도/후기 등록 API (POST /api/v1/users/{target_user_id}/review)
# -----------------------------------------------------------------
@router.post("/{target_user_id}/review", response_model=schemas.ReviewResponse)
def create_review(
    target_user_id: str,
    review: schemas.ReviewCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    [매너온도 평가 및 후기 등록]
    거래 상대방에게 후기를 남기고, 상대방의 매너온도를 갱신합니다.
    (긍정 평가 시 +0.1도, 부정 평가 시 -0.1도)

    Args:
        target_user_id (str): 후기를 받을 상대방의 User ID (UUID)
        review (ReviewCreate): 평가 내용 (좋아요 여부, 평가 키워드 리스트)
        current_user (User): 리뷰를 작성하는 현재 로그인 사용자

    Raises:
        400 Bad Request: 본인에게 리뷰를 남기려고 할 때 발생
    """

    # 1. 본인 리뷰 방지 (Self-Review Check)
    if target_user_id == current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="본인에게 리뷰를 남길 수 없습니다."
        )

    # 2. 리뷰 저장 및 매너온도 계산 (CRUD 계층으로 위임)
    # new_temp: 계산이 완료된 상대방의 새로운 매너온도
    new_review, new_temp = crud.create_review(
        db=db,
        review=review,
        reviewer_id=current_user.user_id,
        target_user_id=target_user_id
    )

    return {
        "review_id": new_review.review_id,
        "target_user_id": target_user_id,
        "new_temperature": new_temp
    }


# -----------------------------------------------------------------
# 3. 사용자 매너온도 조회 API (GET /api/v1/users/{user_id}/manner)
# -----------------------------------------------------------------
@router.get("/{user_id}/manner", response_model=schemas.MannerStatsResponse)
def read_manner_stats(user_id: str, db: Session = Depends(database.get_db)):
    """
    [매너온도 통계 조회]
    특정 사용자의 현재 매너온도와 받은 긍정적인 평가 항목들의 개수를 조회합니다.
    (예: "친절해요": 5회, "시간 약속을 잘 지켜요": 3회)

    Args:
        user_id (str): 조회할 대상의 User ID

    Returns:
        MannerStatsResponse: 매너온도(float), 긍정 리뷰 통계(dict)

    Raises:
        404 Not Found: 해당 ID의 사용자가 없을 경우
    """

    # 1. 사용자 존재 여부 확인
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. 리뷰 통계 계산 (어떤 칭찬을 얼마나 받았는지 카운팅)
    stats = crud.get_reviews_stats(db, user_id)

    return {
        "manner_temperature": user.manner_temperature,
        "positive_reviews": stats
    }