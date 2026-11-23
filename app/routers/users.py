from fastapi import APIRouter
from app.schemas import UserCreate, ProblemDetails

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/register",
    responses={
        422: {
            "description": "Validation Error",
            "content": {
                "application/problem+json": {
                    "schema": ProblemDetails.model_json_schema(),
                    "example": {
                        "type": "https://example.com",
                        "title": "Validation Error",
                        "status": 422,
                        "detail": "The request body failed validation.",
                        "instance": "/users/register",
                        "errors": [
                            {"field": "age", "message": "Input should be greater than 18", "code": "greater_than"},
                            {"field": "email", "message": "value is not a valid email address", "code": "value_error"}
                        ]
                    }
                }
            }
        }
    }
)
async def register(user: UserCreate):
    return {"username": user.username, "email": user.email}
