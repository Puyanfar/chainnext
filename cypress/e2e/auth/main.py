import os
from uuid import uuid4

from fastapi import Request, Response

import chainlit as cl
from chainlit.auth import create_jwt
from chainlit.server import _authenticate_user, app
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


# FastAPI >= 0.165 wraps included routers in _IncludedRouter (no .path), which
# shadows the /auth/* endpoints below. Move the catch-all's wrapper last.
def _move_spa_catch_all_to_end(routes) -> None:
    from fastapi.routing import _IncludedRouter

    catch_all_wrappers = [
        r
        for r in routes
        if isinstance(r, _IncludedRouter)
        and any(
            getattr(route, "path", None) == "/{full_path:path}"
            for route in r.original_router.routes
        )
    ]

    for wrapper in catch_all_wrappers:
        routes.remove(wrapper)
        routes.append(wrapper)


_move_spa_catch_all_to_end(app.router.routes)


@cl.on_chat_start
async def on_chat_start():
    user = cl.user_session.get("user")
    await cl.Message(f"Hello {user.identifier}").send()


@cl.on_message
async def on_message(msg: cl.Message):
    await cl.Message(content=f"Echo: {msg.content}").send()
