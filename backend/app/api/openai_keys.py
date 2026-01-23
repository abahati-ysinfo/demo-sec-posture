"""Admin API endpoints for OpenAI API key management."""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.auth import get_current_admin_user
from app.core.database import get_db
from app.schemas.openai_key import (
    OpenAIKeyCreate,
    OpenAIKeyResponse,
    OpenAIKeyTest,
    OpenAIKeyTestResponse,
    OpenAIKeyToggle,
)
from app.schemas.user import CurrentUserResponse
from app.services.openai_key_manager import OpenAIKeyManager

router = APIRouter()


@router.get("/", response_model=list[OpenAIKeyResponse])
async def list_openai_keys(
    request: Request,
    include_inactive: bool = False,
    current_admin: CurrentUserResponse = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> list[OpenAIKeyResponse]:
    """List all OpenAI API keys with masked values."""
    try:
        with OpenAIKeyManager(db) as manager:
            keys = manager.list_keys(include_inactive=include_inactive)
            return [OpenAIKeyResponse(**k) for k in keys]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list API keys: {str(e)}",
        )


@router.post("/", response_model=OpenAIKeyResponse)
async def create_openai_key(
    request: Request,
    key_data: OpenAIKeyCreate,
    current_admin: CurrentUserResponse = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> OpenAIKeyResponse:
    """Add a new OpenAI API key."""
    try:
        with OpenAIKeyManager(db) as manager:
            key = manager.add_key(
                key_name=key_data.key_name,
                api_key=key_data.api_key,
                created_by=current_admin.email,
            )

            keys = manager.list_keys(include_inactive=True)
            for k in keys:
                if k["id"] == key.id:
                    return OpenAIKeyResponse(**k)

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve created key",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create API key: {str(e)}",
        )


@router.post("/test", response_model=OpenAIKeyTestResponse)
async def test_openai_key(
    request: Request,
    key_data: OpenAIKeyTest,
    current_admin: CurrentUserResponse = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> OpenAIKeyTestResponse:
    """Test if an OpenAI API key is valid."""
    try:
        with OpenAIKeyManager(db) as manager:
            is_valid, message = manager.test_key(key_data.api_key)
            return OpenAIKeyTestResponse(is_valid=is_valid, message=message)
    except Exception as e:
        return OpenAIKeyTestResponse(is_valid=False, message=f"Test failed: {str(e)}")


@router.patch("/{key_id}/toggle", response_model=OpenAIKeyResponse)
async def toggle_openai_key(
    request: Request,
    key_id: str,
    toggle_data: OpenAIKeyToggle,
    current_admin: CurrentUserResponse = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> OpenAIKeyResponse:
    """Toggle an OpenAI API key's active status."""
    try:
        with OpenAIKeyManager(db) as manager:
            manager.toggle_key(key_id, toggle_data.is_active)

            keys = manager.list_keys(include_inactive=True)
            for k in keys:
                if k["id"] == key_id:
                    return OpenAIKeyResponse(**k)

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Key not found after toggle",
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to toggle API key: {str(e)}",
        )


@router.delete("/{key_id}")
async def delete_openai_key(
    request: Request,
    key_id: str,
    current_admin: CurrentUserResponse = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """Delete an OpenAI API key."""
    try:
        with OpenAIKeyManager(db) as manager:
            manager.delete_key(key_id)
            return {"message": "API key deleted successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete API key: {str(e)}",
        )
