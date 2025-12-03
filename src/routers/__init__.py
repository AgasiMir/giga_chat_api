from .handlers import router as handlers_router
from .requests import router as requests_router

routers = [
    handlers_router,
    requests_router
]
