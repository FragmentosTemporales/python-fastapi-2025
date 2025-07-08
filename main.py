from fastapi import FastAPI, Body, HTTPException, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, FileResponse
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(
    title="TestingAPI",
    description="API para testeo de FastAPI",
    version="2.0.1",
)

class Usuario(BaseModel):
    id: int
    name: str = Field(min_length=5, max_length=50, default="Sin Nombre")
    email: str = Field(min_length=10, max_length=50, default="Sin Correo")
    phone: str = Field(min_length=10, max_length=50, default="Sin Telefono")
    password: str = Field(min_length=8, max_length=50, default="Sin Contraseña")
    age: int = Field(gt=18, le=120, default=18)

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Cristian Rivera",
                "email": "cristian.rivera@gmail.com",
                "phone": "+56963410066",
                "password": "secretpass",
                "age": 30
            }
        }
    }

class UsuarioCreate(Usuario):
    id: int
    name: str = Field(min_length=5, max_length=50, example="Cristian Rivera", default="Sin Nombre")
    email: str = Field(min_length=10, max_length=50, example="cristian.rivera@gmail.com", default="Sin Correo")
    phone: str = Field(min_length=10, max_length=50, example="+56963410066", default="Sin Telefono")
    password: str = Field(min_length=8, max_length=50, example="secretpass", default="Sin Contraseña")
    age: int = Field(gt=18, le=120, example=30, default=18)

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Cristian Rivera",
                "email": "cristian.rivera@gmail.com",
                "phone": "+56963410066",
                "password": "secretpass",
                "age": 30
            }
        }
    }

class UsuarioUpdate(BaseModel):
    name: str = Field(min_length=5, max_length=50, example="Cristian Rivera", default="Sin Nombre")
    email: str = Field(min_length=10, max_length=50, example="cristian.rivera@gmail.com", default="Sin Correo")
    phone: str = Field(min_length=10, max_length=50, example="+56963410066", default="Sin Telefono")
    password: str = Field(min_length=8, max_length=50, example="secretpass", default="Sin Contraseña")
    age: int = Field(gt=18, le=120, example=30, default=18)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Cristian Rivera",
                "email": "cristian.rivera@gmail.com",
                "phone": "+56963410066",
                "password": "secretpass",
                "age": 30
            }
        }
    }

class UsuarioPrivate(BaseModel):
    name: str = Field(min_length=5, max_length=50, example="Cristian Rivera", default="Sin Nombre")
    email: str = Field(min_length=10, max_length=50, example="cristian.rivera@gmail.com", default="Sin Correo")
    phone: str = Field(min_length=10, max_length=50, example="+56963410066", default="Sin Telefono")
    age: int = Field(gt=18, le=120, example=30, default=18)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Cristian Rivera",
                "email": "cristian.rivera@gmail.com",
                "phone": "+56963410066",
                "age": 30
            }
        }
    }

usuarios : List[Usuario] = []

@app.get(
        '/',
        tags=["main"],
        status_code=200,
        response_description="Respuesta de bienvenida.")
def main_():
    return PlainTextResponse("Bienvenido a la API de TestingAPI. Puedes acceder a los endpoints de usuario.", status_code=200)


@app.get(
        '/usuarios',
        tags=["usuario"],
        status_code=200,
        response_description="Lista de usuarios.")
def get_usuarios() -> List[Usuario]:
    data = [usuario.model_dump() for usuario in usuarios]
    return JSONResponse(content=data, status_code=200)


@app.get(
        '/usuario/{id}',
        tags=["usuario"],
        status_code=200,
        response_description="Usuario por ID.")
def usuario_(id: int = Path(gt=0)) -> UsuarioPrivate | dict:
    for usuario in usuarios:
        if usuario.id == id:
            data = usuario.model_dump()
            return JSONResponse(content=data, status_code=200)
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@app.get(
        '/usuario/',
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


@app.post(
        '/usuario/',
        tags=["usuario"],
        status_code=303,
        response_description="Crear un nuevo usuario.")
def crear_usuario(usuario: UsuarioCreate) -> List[Usuario]:
    usuarios.append(usuario)
    data = [usuario.model_dump() for usuario in usuarios]
    #return JSONResponse(content=data)
    return RedirectResponse(url="/usuarios", status_code=303)


@app.put(
        '/usuario-update/',
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


@app.delete(
        '/usuario-delete/{id}',
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


@app.get(
        '/get_file',
        tags=["file"],
        status_code=200,
        response_description="Obtener archivo README.md.")
def get_file():
    file_path = "README.md"
    return FileResponse(file_path, filename='README.md', media_type='text/markdown')
