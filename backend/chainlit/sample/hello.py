# This is a simple example of a chainlit app.
# Install the PyPI package with `pip install chainnext`, then run `chainlit hello`.

from chainlit import AskUserMessage, Message, on_chat_start


@on_chat_start
async def main():
    res = await AskUserMessage(content="What is your name?", timeout=30).send()
    if res:
        await Message(
            content=(
                f"Your name is: {res['output']}.\n"
                "Chainnext installation is working!\n"
                "Keep using `import chainlit` and the `chainlit` CLI in your apps."
            ),
        ).send()
