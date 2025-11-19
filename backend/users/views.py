from ninja import Router 
from ninja_jwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .schemas import UserInRegisterSchema, UserOutSchema, UserInLoginSchema, LoginOutSchema
from core.schemas import ErrorSchema
from core.helper_error import error_response
from .helper import *


router = Router() 

@router.post('/register', response={201: LoginOutSchema, 409: ErrorSchema}, auth=None)
def create_user(request, payload: UserInRegisterSchema):
    if User.objects.filter(email=payload.email).exists():
        return error_response("EMAIL_EXISTS", 409)
    username = create_username(payload.nome)
    user = User.objects.create_user(
        username=username, 
        email=payload.email, 
        password=payload.password
    )
    user.refresh_from_db()
    refresh = RefreshToken.for_user(user)
    return 201, {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": user
    }

@router.post('/login', response={200: LoginOutSchema, 401: ErrorSchema, 404: dict}, auth=None)
def login_user(request, payload: UserInLoginSchema):
    try:
        user = User.objects.get(email=payload.email)
    except User.DoesNotExist:
        return error_response("USER_NOT_FOUND", 404)
    
    user = authenticate(request, username=user.username, password=payload.password)
    if not user:
        return error_response("INVALID_CREDENTIALS", 401)
    
    refresh = RefreshToken.for_user(user)
    return 200, {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": user
    }

@router.get('/me', response=LoginOutSchema, auth=None)
def get_current_user(request):
    """Endpoint protegido - usa o token automaticamente"""
    user= request.user
    refresh = RefreshToken.for_user(user)
    return 200, {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": user
    }