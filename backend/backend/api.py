from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI
from ninja_jwt.authentication import JWTAuth
from receipts.views import router as receipts_router
from sandbox.views import router as sandbox_router
from users.views import router as user_router


api = NinjaExtraAPI(auth=JWTAuth())  
api.register_controllers(NinjaJWTDefaultController)

api.add_router("/receipts/", receipts_router)
api.add_router("/sandbox/", sandbox_router)
api.add_router("/user/", user_router)

