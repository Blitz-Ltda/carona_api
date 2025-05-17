from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class NotFoundError(Exception):
    def __init__(self, name: str):
        self.name = name

async def not_found_exception_handler(_: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={"message": f"Oops! {exc.name} not found."},
    )