from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    
    custom_error_messages = []
    for error in errors:
        loc = error["loc"]
        msg = error["msg"]
        field = loc[-1]
        custom_error_messages.append(f"{field}: {msg}")

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": custom_error_messages},
    )