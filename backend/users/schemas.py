from ninja import Schema, ModelSchema
from pydantic import field_validator
from django.contrib.auth.models import User

class UserInRegisterSchema(Schema):
    nome: str
    email: str
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('A senha deve ter pelo menos 8 caracteres')
        if len(v) > 24:
            raise ValueError('A senha não pode ter mais de 24 caracteres')
        return v

class UserInLoginSchema(Schema):
    email: str
    password: str

class UserOutSchema(ModelSchema):
    class Meta: 
        model = User
        exclude = ['password']

class LoginOutSchema(Schema):
    access: str
    refresh: str
    user: UserOutSchema
