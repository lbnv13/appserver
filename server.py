# async
import uvicorn
# FastAPI
from fastapi import FastAPI, Request
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse
# routers
from auth.router import router as auth_router

# app
app = FastAPI(
    title="app server"
)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


# including routers
app.include_router(auth_router)

# run
if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')
