from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="TestingAPI",
    description="API para testeo de FastAPI",
    version="2.0.1",
)

class Usuario(BaseModel):
    id: int
    nome: str
    email: str
    telefone: str
    password: str

class UsuarioUpdate(BaseModel):
    nome: str
    email: str
    telefone: str
    password: str

class UsuarioPrivate(BaseModel):
    nome: str
    email: str
    telefone: str

usuarios = [
    {"id": 1, "nome": "João", "email": "example1@mail.com", "telefone": "123456789", "password": "123456"},
    {"id": 2, "nome": "Maria", "email": "example2@mail.com", "telefone": "123456789", "password": "123456"},
    {"id": 3, "nome": "José", "email": "example3@mail.com", "telefone": "123456789", "password": "123456"}
]

@app.get('/', tags=["main"])
def main_():
    return {"message": "Hello, World!"}


@app.get('/usuarios', tags=["usuario"])
def get_usuarios() -> List[Usuario]:
    return usuarios


@app.get('/usuario/{id}', tags=["usuario"])
def usuario_(id: int) -> UsuarioPrivate:
    for usuario in usuarios:
        if usuario["id"] == id:
            return usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@app.get('/usuario/', tags=["usuario"])
def usuarios_(nombre: str = None) -> Usuario:
    if nombre is not None:
        for usuario in usuarios:
            if usuario["nome"].lower() == nombre.lower():
                return usuario
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    raise HTTPException(status_code=400, detail="Debe proporcionar un nombre o un ID")


@app.post('/usuario/', tags=["usuario"])
def crear_usuario(usuario: Usuario):
    usuarios.append(usuario.model_dump())
    return {"message": "Usuario creado exitosamente", "usuario": usuario}


@app.put('/usuario-update/', tags=["usuario"])
def atualizar_usuario(usuarioUpdate: UsuarioUpdate, id: int = Body()) -> Usuario:
    
    for usuario in usuarios:
        if usuario["id"] == id:
            if usuarioUpdate.nome is not None:
                usuario["nome"] = usuarioUpdate.nome
            if usuarioUpdate.email is not None:
                usuario["email"] = usuarioUpdate.email
            if usuarioUpdate.telefone is not None:
                usuario["telefone"] = usuarioUpdate.telefone
            if usuarioUpdate.password is not None:
                usuario["password"] = usuarioUpdate.password

            return {"message": "Usuario actualizado exitosamente", "usuario": usuario}

    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@app.delete('/usuario-delete/{id}', tags=["usuario"])
def eliminar_usuario(id: int):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuarios.remove(usuario)
            return {"message": "Usuario eliminado"}
    
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
