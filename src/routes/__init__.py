from src.routes.auth import router as auth_router
from src.routes.health import router as health_router


list_of_routes = [health_router, auth_router]


__all__ = ["list_of_routes"]
