from .settings import settings_router
from .user import user_router

routers_list = [
    user_router,
    settings_router,
]
