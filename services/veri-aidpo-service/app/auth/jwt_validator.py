"""
JWT Token Validation Middleware for VeriAIDPO Service

This module validates JWT tokens from the main backend and extracts user claims.
Tokens are validated using the shared JWT secret key from configuration.
"""

from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.config import settings

# HTTPBearer security scheme for JWT authentication
security = HTTPBearer()


async def validate_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> dict:
    """
    Validate JWT token from main backend and extract user claims.
    
    Args:
        credentials: HTTPAuthorizationCredentials containing the Bearer token
        
    Returns:
        dict: User information containing:
            - user_id: User's unique identifier
            - role: User's role (admin, dpo, staff, auditor, viewer)
            - tenant_id: User's tenant/company identifier
            - permissions: List of user permissions
            
    Raises:
        HTTPException: 401 if token is invalid or missing required claims
        
    Example:
        ```python
        @router.post("/classify")
        async def classify(user: dict = Depends(validate_token)):
            # User is authenticated
            user_id = user["user_id"]
            permissions = user["permissions"]
        ```
    """
    try:
        # Extract token from credentials
        token = credentials.credentials
        
        # Decode JWT token using shared secret
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        
        # Extract user claims from payload
        user_id = payload.get("sub")  # Subject (user ID)
        role = payload.get("role")
        tenant_id = payload.get("tenant_id")
        permissions = payload.get("permissions", [])
        
        # Validate required claims
        if not user_id:
            raise HTTPException(
                status_code=401,
                detail={
                    "error": "Invalid token: missing subject",
                    "error_vi": "Token không hợp lệ: thiếu thông tin người dùng"
                }
            )
        
        # Return user information
        return {
            "user_id": user_id,
            "role": role,
            "tenant_id": tenant_id,
            "permissions": permissions
        }
        
    except JWTError as e:
        # Token validation failed (invalid signature, expired, malformed)
        raise HTTPException(
            status_code=401,
            detail={
                "error": f"Token validation failed: {str(e)}",
                "error_vi": f"Xác thực token thất bại: {str(e)}"
            }
        )
    except Exception as e:
        # Unexpected error during validation
        raise HTTPException(
            status_code=401,
            detail={
                "error": f"Authentication error: {str(e)}",
                "error_vi": f"Lỗi xác thực: {str(e)}"
            }
        )
