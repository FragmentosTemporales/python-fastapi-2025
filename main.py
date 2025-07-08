from fastapi import FastAPI, Body, HTTPException, Path, Query
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

@app.get('/', tags=["main"])
def main_():
    return {"message": "Hello, World!"}


@app.get('/usuarios', tags=["usuario"])
def get_usuarios() -> List[Usuario]:
    return [usuario.model_dump() for usuario in usuarios]


@app.get('/usuario/{id}', tags=["usuario"])
def usuario_(id: int = Path(gt=0)) -> UsuarioPrivate | dict:
    for usuario in usuarios:
        if usuario.id == id:
            return usuario.model_dump()
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@app.get('/usuario/', tags=["usuario"])
def usuarios_(nombre: str = None) -> Usuario:
    if nombre is not None:
        for usuario in usuarios:
            if usuario.name.lower() == nombre.lower():
                return usuario.model_dump()
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    raise HTTPException(status_code=400, detail="Debe proporcionar un nombre o un ID")


@app.post('/usuario/', tags=["usuario"])
def crear_usuario(usuario: UsuarioCreate) -> List[Usuario]:
    usuarios.append(usuario)
    return [usuario.model_dump() for usuario in usuarios]


@app.put('/usuario-update/', tags=["usuario"])
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

            return usuario.model_dump()

    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@app.delete('/usuario-delete/{id}', tags=["usuario"])
def eliminar_usuario(id: int) -> List[Usuario]:
    for usuario in usuarios:
        if usuario.id == id:
            usuarios.remove(usuario)
            return [usuario.model_dump() for usuario in usuarios]
    
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
