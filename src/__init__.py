import os
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from rich import print

from src.utils.http_error_handler import HTTPErrorHandler
from src.routes.usuario_router import usuario_router
from src.routes.file_router import file_router

from src.sql import MyEngine

# INICIALIZACIÓN DE LA APLICACIÓN
def create_app(test_mode=False):

    app = FastAPI(
        title="TestingAPI",
        description="API para testeo de FastAPI",
        version="2.0.1"
    )


    static_path = os.path.join(os.path.dirname(__file__), 'static')
    templates_path = os.path.join(os.path.dirname(__file__), 'templates')

    app.mount('/static', StaticFiles(directory=static_path), name='static')
    templates = Jinja2Templates(directory=templates_path)

    app.add_middleware(HTTPErrorHandler)

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

    return app