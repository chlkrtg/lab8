from fastapi import FastAPI
from app.config import settings
from app.routers import users_router, test_router
from app.exceptions import CustomExceptionA, CustomExceptionB
from app.handlers import custom_exception_a_handler, custom_exception_b_handler

app = FastAPI(title=settings.app_name)

app.add_exception_handler(CustomExceptionA, custom_exception_a_handler)
app.add_exception_handler(CustomExceptionB, custom_exception_b_handler)

app.include_router(users_router)
app.include_router(test_router)


@app.get("/")
async def root():
    return {"message": "Hello, Error Handling Lab!"}
