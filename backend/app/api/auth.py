from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import (
    AUTH_COOKIE_NAME,
    clear_auth_cookie,
    create_access_token,
    get_password_hash,
    set_auth_cookie,
    verify_password,
    verify_token,
)
from app.middleware.rate_limit import limiter
from app.models.user import User
from app.schemas.user import (
    CurrentUserResponse,
    Token,
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.services.security_metrics import security_metrics

router = APIRouter()
security = HTTPBearer()
security_optional = HTTPBearer(auto_error=False)


@limiter.limit("5/minute")
@router.post("/register", response_model=Token)
async def register(
    request: Request,
    response: Response,
    user_data: UserCreate,
    db: Session = Depends(get_db),
) -> Token:
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        company_name=user_data.company_name,
        password_hash=hashed_password,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token, csrf_token = create_access_token(
        data={
            "sub": db_user.email,
            "user_id": str(db_user.id),
            "is_admin": db_user.is_admin if hasattr(db_user, "is_admin") else False,
        }
    )

    if settings.ENABLE_COOKIE_AUTH:
        max_age = settings.ACCESS_TOKEN_EXPIRE_HOURS * 3600
        set_auth_cookie(response, access_token, max_age)
        security_metrics.increment_cookie_auth()

    return Token(
        access_token=access_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_HOURS * 3600,
        user=UserResponse.model_validate(db_user),
        csrf_token=csrf_token if settings.ENABLE_CSRF else None,
    )


@limiter.limit("5/minute")
@router.post("/login", response_model=Token)
async def login(
    request: Request,
    response: Response,
    user_credentials: UserLogin,
    db: Session = Depends(get_db),
) -> Token:
    if user_credentials.email == settings.ADMIN_EMAIL:
        if not settings.ADMIN_PASSWORD_HASH:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Admin password not configured",
            )

        if not verify_password(user_credentials.password, settings.ADMIN_PASSWORD_HASH):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        access_token, csrf_token = create_access_token(
            data={"sub": settings.ADMIN_EMAIL, "is_admin": True}, is_admin=True
        )

        if settings.ENABLE_COOKIE_AUTH:
            max_age = settings.ADMIN_TOKEN_EXPIRE_HOURS * 3600
            set_auth_cookie(response, access_token, max_age)
            security_metrics.increment_cookie_auth()

        return Token(
            access_token=access_token,
            expires_in=settings.ADMIN_TOKEN_EXPIRE_HOURS * 3600,
            csrf_token=csrf_token if settings.ENABLE_CSRF else None,
        )

    user = db.query(User).filter(User.email == user_credentials.email).first()
    if not user or not verify_password(
        user_credentials.password, str(user.password_hash)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    access_token, csrf_token = create_access_token(
        data={
            "sub": user.email,
            "user_id": str(user.id),
            "is_admin": user.is_admin if hasattr(user, "is_admin") else False,
        }
    )

    if settings.ENABLE_COOKIE_AUTH:
        max_age = settings.ACCESS_TOKEN_EXPIRE_HOURS * 3600
        set_auth_cookie(response, access_token, max_age)
        security_metrics.increment_cookie_auth()

    return Token(
        access_token=access_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_HOURS * 3600,
        user=UserResponse.model_validate(user),
        csrf_token=csrf_token if settings.ENABLE_CSRF else None,
    )


async def get_current_user_from_token(token: str, db: Session) -> CurrentUserResponse:
    """Extract user from JWT token"""
    token_data = verify_token(token)

    if token_data.get("is_admin"):
        if token_data.get("user_id"):
            user = db.query(User).filter(User.id == token_data["user_id"]).first()
            if user:
                return CurrentUserResponse.model_validate(user)

        return CurrentUserResponse(
            id="admin",
            email=settings.ADMIN_EMAIL,
            full_name="Administrator",
            company_name="EchoStor",
            is_admin=True,
            is_active=True,
        )

    email = token_data.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return CurrentUserResponse.model_validate(user)


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(security_optional),
    db: Session = Depends(get_db),
) -> CurrentUserResponse:
    """Unified auth dependency: checks cookie first (if enabled), then Authorization header"""
    token = None

    if settings.ENABLE_COOKIE_AUTH:
        token = request.cookies.get(AUTH_COOKIE_NAME)
        if token:
            security_metrics.increment_cookie_auth()

    if not token and credentials:
        token = credentials.credentials

    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authenticated",
        )

    return await get_current_user_from_token(token, db)


async def get_current_admin_user(
    current_user: CurrentUserResponse = Depends(get_current_user),
) -> CurrentUserResponse:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )
    return current_user


@router.get("/csrf")
async def get_csrf_token(request: Request) -> dict[str, str]:
    """Get CSRF token from current JWT for client-side storage"""
    if not settings.ENABLE_CSRF or not settings.ENABLE_COOKIE_AUTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CSRF protection not enabled",
        )

    auth_cookie = request.cookies.get(AUTH_COOKIE_NAME)
    if not auth_cookie:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    try:
        token_data = verify_token(auth_cookie)
        csrf_token = token_data.get("csrf", "")
        if not csrf_token:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="CSRF token not found in JWT",
            )
        return {"csrf_token": csrf_token}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve CSRF token",
        )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response) -> None:
    """Clear authentication cookie"""
    if settings.ENABLE_COOKIE_AUTH:
        clear_auth_cookie(response)
    return None


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    request: Request,
    current_user: CurrentUserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserResponse:
    if current_user.is_admin and current_user.id == "admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin user info not available",
        )

    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return UserResponse.model_validate(user)
