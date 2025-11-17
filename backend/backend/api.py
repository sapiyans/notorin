from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI
from ninja_jwt.authentication import JWTAuth
from sandbox.views import router as sandbox_router



api = NinjaExtraAPI()  
api.register_controllers(NinjaJWTDefaultController)
api.add_router("/sandbox/", sandbox_router)

