import logging

import jwt
from starlette.applications import Starlette
from starlette.authentication import (AuthCredentials, AuthenticationBackend,
                                      SimpleUser, UnauthenticatedUser)
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.responses import PlainTextResponse
from starlette.routing import Route

logger = logging.getLogger("myapp")

KEY = "secret"


class AnonymousUser(UnauthenticatedUser):
    """Anonymous User"""
    @property
    def username(self):
        return "anonymous"


class JWTAuthenticationBackend(AuthenticationBackend):
    """JWT Authentication Backend"""
    async def authenticate(self, request):
        auth_token = request.headers.get("token") or request.query_params.get("token")
        logger.debug("auth_token: {auth_token}"  )
        if auth_token is None:
            return AuthCredentials(scopes=["anonymous"]), AnonymousUser()

        try:
            jwt.decode(auth_token, KEY, algorithms=["HS256"])
            logger.warning("JWT token valid")
            return AuthCredentials(["authenticated"]), SimpleUser("nikos")
        except jwt.ExpiredSignatureError:
            logger.warning("JWT token expired")
            return AuthCredentials(["anonymous"]), AnonymousUser()
        except jwt.InvalidTokenError:
            logger.warning("Invalid JWT token")
            return AuthCredentials(["anonymous"]), AnonymousUser()


async def homepage(request):
    """Homepage"""
    user = request.user
    return PlainTextResponse(f"Hello, {user.username}!")


routes = [Route("/", homepage)]
middleware = [Middleware(AuthenticationMiddleware, backend=JWTAuthenticationBackend())]
app = Starlette(routes=routes, middleware=middleware)
