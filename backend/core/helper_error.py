ERRORS = {
    "EMAIL_EXISTS": "Email já existe",
    "INVALID_CREDENTIALS": "Credenciais inválidas",
    "USER_NOT_FOUND": "Usuário não encontrado",
}

def error_response(code: str, status: int):
    return status, {
        "error": {
            "code": code,
            "message": ERRORS.get(code, "Erro desconhecido")
        }
    }