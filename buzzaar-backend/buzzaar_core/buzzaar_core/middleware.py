import jwt
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken

from users.models import CustomUser as User


@database_sync_to_async
def get_user(token_key):
    try:
        payload = UntypedToken(token_key)
        user_id = payload.get("user_id")
        return User.objects.get(id=user_id)
    except (User.DoesNotExist, InvalidToken, TokenError, jwt.ExpiredSignatureError):
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = dict(scope["headers"])
        if b"cookie" in headers:
            cookie_items = dict(
                x.split("=")
                for x in headers[b"cookie"].decode().replace(" ", "").split(";")
            )
            if "buzzaar_access_token" in cookie_items:
                token = cookie_items["buzzaar_access_token"]
                scope["user"] = await get_user(token)
            return await super().__call__(scope, receive, send)
