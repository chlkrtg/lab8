import uuid
from fastapi import FastAPI, Request
from app.config import settings
from app.routers import users_router, test_router
from app.exceptions import CustomExceptionA, CustomExceptionB
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.handlers import (
    custom_exception_a_handler,
    custom_exception_b_handler,
    global_exception_handler,
    validation_exception_handler,
    http_exception_handler,
)

app = FastAPI(title=settings.app_name)

app.add_exception_handler(CustomExceptionA, custom_exception_a_handler)
app.add_exception_handler(CustomExceptionB, custom_exception_b_handler)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)

app.include_router(users_router)
app.include_router(test_router)


@app.get("/")
async def root():
    return {"message": "Hello, Error Handling Lab!"}


@app.middleware("http")
async def add_request_id_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
