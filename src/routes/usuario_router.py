from fastapi import FastAPI, Body, HTTPException, Path, Query, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, FileResponse
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

from src.models.usuario_model import * 


# RUTAS

usuarios : List[Usuario] = []


usuario_router = APIRouter()


@usuario_router.get(
        '/',
        tags=["usuario"],
        status_code=200,
        response_description="Lista de usuarios.")
def get_usuarios() -> List[Usuario]:
    data = [usuario.model_dump() for usuario in usuarios]
    return JSONResponse(content=data, status_code=200)


@usuario_router.get(
        '/{id}',
        tags=["usuario"],
        status_code=200,
        response_description="Usuario por ID.")
def usuario_(id: int = Path(gt=0)) -> BaseUsuario | dict:
    for usuario in usuarios:
        if usuario.id == id:
            data = usuario.model_dump()
            return JSONResponse(content=data, status_code=200)
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@usuario_router.get(
        '/by_name',
        tags=["usuario"],
        status_code=200,
        response_description="Usuario por nombre.")
def usuarios_(nombre: str = Query(min_length=5, max_length=20)) -> Usuario | dict:
    if nombre is not None:
        for usuario in usuarios:
            if usuario.name.lower() == nombre.lower():
                data = usuario.model_dump()
                return JSONResponse(content=data, status_code=200)
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    raise HTTPException(status_code=400, detail="Debe proporcionar un nombre o un ID")


@usuario_router.post(
        '/',
        tags=["usuario"],
        status_code=303,
        response_description="Crear un nuevo usuario.")
def crear_usuario(usuario: Usuario) -> List[Usuario]:
    usuarios.append(usuario)
    data = [usuario.model_dump() for usuario in usuarios]
    #return JSONResponse(content=data)
    return RedirectResponse(url="/usuarios", status_code=303)


@usuario_router.put(
        '/',
        tags=["usuario"],
        status_code=201,
        response_description="Actualizar un usuario existente.")
def atualizar_usuario(usuarioUpdate: UsuarioUpdate, id: int = Body()) -> Usuario:
    for usuario in usuarios:
        if usuario.id == id:
            if usuarioUpdate.name is not None:
                usuario.name = usuarioUpdate.name
            if usuarioUpdate.email is not None:
                usuario.email = usuarioUpdate.email
            if usuarioUpdate.phone is not None:
                usuario.phone = usuarioUpdate.phone
            if usuarioUpdate.password is not None:
                usuario.password = usuarioUpdate.password
            if usuarioUpdate.age is not None:
                usuario.age = usuarioUpdate.age

            data = usuario.model_dump()
            return JSONResponse(content=data, status_code=201)

    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@usuario_router.delete(
        '/{id}',
        tags=["usuario"],
        status_code=200,
        response_description="Eliminar un usuario por ID.")
def eliminar_usuario(id: int) -> List[Usuario]:
    for usuario in usuarios:
        if usuario.id == id:
            usuarios.remove(usuario)
            data = [usuario.model_dump() for usuario in usuarios]
            return JSONResponse(content=data, status_code=200)

    raise HTTPException(status_code=404, detail="Usuario no encontrado")

