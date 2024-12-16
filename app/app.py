from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routes import countries, cities, temperatures

app = FastAPI()


@app.get("/")
def health_check():
    return {"status": "ok"}


async def custom_request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )


app.add_exception_handler(
    RequestValidationError, custom_request_validation_exception_handler
)
app.include_router(countries.router, prefix="/api/countries", tags=["Countries"])
app.include_router(cities.router, prefix="/api/cities", tags=["Cities"])
app.include_router(
    temperatures.router, prefix="/api/temperatures", tags=["Temperatures"]
)
