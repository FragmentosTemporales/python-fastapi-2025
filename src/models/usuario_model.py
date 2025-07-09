
from pydantic import BaseModel, Field, field_validator

# MODELOS


class BaseUsuario(BaseModel):
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
    @field_validator('name')
    def validate_name(cls, value: str) -> str:
        if len(value) < 5 or len(value) > 50:
            raise ValueError("El nombre debe tener entre 5 y 50 caracteres.")
        return value

    @field_validator('email')
    def validate_email(cls, value: str) -> str:
        if len(value) < 10 or len(value) > 50:
            raise ValueError("El correo debe tener entre 10 y 50 caracteres.")
        return value

    @field_validator('email')
    def validate_email_format(cls, value: str) -> str:
        if "@" not in value or "." not in value:
            raise ValueError("El correo debe tener un formato válido.")
        return value

    @field_validator('phone')
    def validate_phone(cls, value: str) -> str:
        if len(value) < 10 or len(value) > 50:
            raise ValueError("El teléfono debe tener entre 10 y 50 caracteres.")
        if not value.startswith("+") or not value[1:].isdigit():
            raise ValueError("El teléfono debe comenzar con '+' y contener solo dígitos después.")
        return value

    @field_validator('age')
    def validate_age(cls, value: int) -> int:
        if value < 18 or value > 120:
            raise ValueError("La edad debe estar entre 18 y 120 años.")
        return value


class Usuario(BaseUsuario):
    """Modelo de Usuario
    Este modelo representa un usuario con sus atributos básicos como id, nombre, correo electrónico, teléfono, contraseña y edad.
    """
    id: int
    password: str = Field(min_length=8, max_length=50, default="Sin Contraseña")
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

    @field_validator('password')
    def validate_password(cls, value: str) -> str:
        if len(value) < 8 or len(value) > 50:
            raise ValueError("La contraseña debe tener entre 8 y 50 caracteres.")
        if not any(char.isdigit() for char in value):
            raise ValueError("La contraseña debe contener al menos un dígito.")
        if not any(char.isalpha() for char in value):
            raise ValueError("La contraseña debe contener al menos una letra.")
        return value


class UsuarioUpdate(BaseUsuario):
    password: str = Field(min_length=8, max_length=50, example="secretpass", default="Sin Contraseña")
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

    @field_validator('password')
    def validate_password(cls, value: str) -> str:
        if len(value) < 8 or len(value) > 50:
            raise ValueError("La contraseña debe tener entre 8 y 50 caracteres.")
        if not any(char.isdigit() for char in value):
            raise ValueError("La contraseña debe contener al menos un dígito.")
        if not any(char.isalpha() for char in value):
            raise ValueError("La contraseña debe contener al menos una letra.")
        return value
