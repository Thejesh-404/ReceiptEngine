from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.routes import router as api_router
from app.api.exceptions import  validation_exception_handler

app = FastAPI()

app.include_router(api_router,  prefix="/api/v1")

app.add_exception_handler(RequestValidationError, validation_exception_handler)

@app.get("/")
async def root():
    return {"message": "Welcome to the Receipt Engine API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)