from ninja import Schema

class ErrorDetail(Schema):
    code: str
    message: str

class ErrorSchema(Schema):
    error: ErrorDetail