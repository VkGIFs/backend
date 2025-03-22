from backend.routes.auth import router as auth_router
from backend.routes.health import router as health_router


list_of_routes = [health_router, auth_router]


__all__ = ["list_of_routes"]
