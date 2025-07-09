from fastapi import FastAPI, status
from fastapi.responses import PlainTextResponse
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

from src.routes.usuario_router import usuario_router
from src.routes.file_router import file_router

#from src.utils.http_error_handler import HTTPErrorHandler

# INICIALIZACIÓN DE LA APLICACIÓN


app = FastAPI(
    title="TestingAPI",
    description="API para testeo de FastAPI",
    version="2.0.1"
)

static_path = os.path.join(os.path.dirname(__file__), 'static')
templates_path = os.path.join(os.path.dirname(__file__), 'templates')

app.mount('/static', StaticFiles(directory=static_path), name='static')
templates = Jinja2Templates(directory=templates_path)

#app.add_middleware(HTTPErrorHandler)
@app.middleware('http')
async def http_error_handler(request : Request, call_next) -> Response | JSONResponse:
    try:
        return await call_next(request)
    except Exception as e:
        content = f"exc: {str(e)}"
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return JSONResponse(
            status_code=status_code,
            content= content
        )


# RUTAS


@app.get(
        '/',
        tags=["main"],
        status_code=200,
        response_description="Respuesta de bienvenida.")
def main_( request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, 
         "message": "Bienvenido a la API de TestingAPI. Puedes acceder a los endpoints de usuario."}
    )


app.include_router(
    usuario_router,
    prefix="/usuarios",
    tags=["usuario"],
    responses={404: {"description": "No encontrado"}}
)
app.include_router(
    file_router,
    prefix="/files",
    tags=["file"],
    responses={404: {"description": "No encontrado"}}
)

