import os
from uuid import uuid4

from fastapi import Request, Response

import chainlit as cl
from chainlit.auth import create_jwt
from chainlit.server import _authenticate_user, app, ensure_spa_fallback_last
from chainlit.user import User

os.environ["CHAINLIT_AUTH_SECRET"] = "SUPER_SECRET"  # nosec B105
os.environ["CHAINLIT_CUSTOM_AUTH"] = "true"


@app.get("/auth/custom")
async def custom_auth(request: Request) -> Response:
    user_id = str(uuid4())

    user = User(identifier=user_id, metadata={"role": "user"})
    response = await _authenticate_user(request, user)

    return response


@app.get("/auth/token")
async def custom_token_auth() -> Response:
    user_id = str(uuid4())

    user = User(identifier=user_id, metadata={"role": "admin"})
    response = create_jwt(user)

    return response


# FastAPI >= 0.137 keeps included routers in app.routes as a tree. Move the SPA
# fallback last so the /auth/* endpoints above are reachable.
ensure_spa_fallback_last()


@cl.on_chat_start
async def on_chat_start():
    user = cl.user_session.get("user")
    await cl.Message(f"Hello {user.identifier}").send()


@cl.on_message
async def on_message(msg: cl.Message):
    await cl.Message(content=f"Echo: {msg.content}").send()
