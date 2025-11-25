# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, database, crud, deps

# 라우터 설정
# prefix: 이 파일의 모든 API URL 앞에 '/api/v1/auth'가 자동으로 붙습니다.
# tags: Swagger UI에서 'Auth'라는 그룹으로 묶여서 보입니다.
router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

# =================================================================
# 1. 회원가입 API (POST /api/v1/auth/signup)
# =================================================================
@router.post("/signup", status_code=201)
def signup(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """
    [회원가입]
    사용자 정보를 입력받아 새로운 회원을 생성합니다.

    Args:
        user (UserCreate): 이메일, 비밀번호, 이름, 닉네임, 지역정보 포함
        db (Session): 데이터베이스 연결 세션

    Returns:
        dict: 생성된 사용자의 고유 ID(user_id), 이메일, 닉네임

    Raises:
        400 Bad Request: 이미 가입된 이메일일 경우 에러 발생
    """

    # 1. 이메일 중복 검사 (이미 가입된 이메일인지 확인)
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered" # 이미 등록된 이메일입니다.
        )

    # 2. 사용자 생성 (비밀번호 암호화는 crud 내부에서 처리됨)
    new_user = crud.create_user(db=db, user=user)

    # 3. 결과 반환 (보안상 비밀번호는 제외하고 필요한 정보만 리턴)
    return {
        "user_id": new_user.user_id,
        "email": new_user.email,
        "nickname": new_user.nickname
    }

# =================================================================
# 2. 로그인 API (POST /api/v1/auth/login)
# =================================================================
@router.post("/login", response_model=schemas.Token)
def login(user_req: schemas.LoginRequest, db: Session = Depends(database.get_db)):
    """
    [로그인]
    이메일과 비밀번호를 검증하고, 인증 성공 시 JWT 토큰을 발급합니다.

    Args:
        user_req (LoginRequest): 로그인하려는 이메일과 비밀번호
        db (Session): 데이터베이스 연결 세션

    Returns:
        Token: access_token과 token_type(bearer) 반환

    Raises:
        401 Unauthorized: 이메일이 없거나 비밀번호가 틀린 경우
    """

    # 1. 이메일로 사용자 조회
    user = crud.get_user_by_email(db, email=user_req.email)

    # 2. 사용자 검증 & 비밀번호 검증
    # deps.verify_password: 입력받은 비밀번호(평문)와 DB의 해시된 비밀번호를 비교
    if not user or not deps.verify_password(user_req.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password", # 보안을 위해 아이디/비번 중 뭐가 틀렸는지 알려주지 않음
        )

    # 3. 액세스 토큰(JWT) 발급
    # subject에는 사용자를 식별할 수 있는 값(여기선 이메일)을 넣음
    access_token = deps.create_access_token(subject=user.email)

    # 4. 토큰 반환 (프론트엔드는 이 토큰을 저장해서 인증에 사용함)
    return {"access_token": access_token, "token_type": "bearer"}