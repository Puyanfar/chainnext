<h1 align="center">Welcome to Chainnext 👋</h1>

<p align="center">
<b>Build python production-ready conversational AI applications in minutes, not weeks ⚡️</b>
</p>

<p align="center">
    <a href="https://pypi.org/project/chainnext" rel="nofollow"><img alt="PyPI" src="https://img.shields.io/pypi/v/chainnext" style="max-width:100%;"></a>
    <a href="https://pypi.org/project/chainnext" rel="nofollow"><img alt="Downloads" src="https://img.shields.io/pypi/dm/chainnext" style="max-width:100%;"></a>
    <a href="https://github.com/Puyanfar/chainnext/graphs/contributors" rel="nofollow"><img alt="Contributors" src="https://img.shields.io/github/contributors/Puyanfar/chainnext" style="max-width:100%;"></a>
    <a href="https://github.com/Puyanfar/chainnext/actions/workflows/ci.yaml" rel="nofollow"><img alt="CI" src="https://github.com/Puyanfar/chainnext/actions/workflows/ci.yaml/badge.svg" style="max-width:100%;"></a>
</p>

Chainnext is a fork of the archived [Chainlit](https://github.com/Chainlit/chainlit) project. The goal is to keep the familiar Chainlit app API while distributing a maintained package under a new name.

<p align="center">
    <a href="https://github.com/Puyanfar/chainnext"><b>Repository</b></a>  •
    <a href="https://docs.chainlit.io"><b>Upstream Chainlit docs</b></a>  •
    <a href="https://github.com/Chainlit/cookbook"><b>Upstream cookbook</b></a>
</p>

## Names: PyPI vs import vs CLI

The **PyPI / GitHub name is `chainnext`**. The **Python import, CLI, and on-disk config names stay `chainlit`** so existing apps keep working.

| What                  | Name          | Example                                            |
| --------------------- | ------------- | -------------------------------------------------- |
| GitHub repository     | `chainnext`   | `https://github.com/Puyanfar/chainnext`            |
| PyPI package          | `chainnext`   | `pip install chainnext`                            |
| Python import         | `chainlit`    | `import chainlit as cl` / `from chainlit import *` |
| CLI                   | `chainlit`    | `chainlit run app.py` / `chainlit hello`           |
| Config directory      | `.chainlit/`  | `.chainlit/config.toml`                            |
| Welcome file          | `chainlit.md` | project-root markdown shown in the UI              |
| Environment variables | `CHAINLIT_*`  | `CHAINLIT_AUTH_SECRET`, `CHAINLIT_PORT`, …         |

Do **not** `pip install chainlit` for this fork, and do **not** `import chainnext` — that module does not exist.

## Installation

Chainnext requires **Python 3.15.2 or newer**. Open a terminal and run:

```sh
pip install chainnext
chainlit hello
```

If this opens the `hello app` in your browser, you're all set!

### Development version

The latest in-development version can be installed straight from GitHub with:

```sh
pip install git+https://github.com/Puyanfar/chainnext.git#subdirectory=backend/
```

(Requires Node.js 26.13.1+, npm 12.2.3+, and pnpm 12.22.0.)

## 🚀 Quickstart

### 🐍 Pure Python

Create a new file `demo.py` with the following code:

```python
import chainlit as cl


@cl.step(type="tool")
async def tool():
    # Fake tool
    await cl.sleep(2)
    return "Response from the tool!"


@cl.on_message  # this function will be called every time a user inputs a message in the UI
async def main(message: cl.Message):
    """
    This function is called every time a user inputs a message in the UI.
    It sends back an intermediate response from the tool, followed by the final answer.

    Args:
        message: The user's message.

    Returns:
        None.
    """

    # Call the tool
    tool_res = await tool()

    await cl.Message(content=tool_res).send()
```

Now run it!

```sh
chainlit run demo.py -w
```

<img src="/images/quick-start.png" alt="Quick Start"></img>

## 📚 More Examples - Cookbook

You can find various examples of Chainlit-compatible apps [here](https://github.com/Chainlit/cookbook) that leverage tools and services such as OpenAI, Anthropic, LangChain, LlamaIndex, ChromaDB, Pinecone and more.

Tell us what you would like to see added in Chainnext using the GitHub issues.

## 💁 Contributing

We welcome bug fixes and security fixes. At this time, pull requests that introduce new features are not reviewed or merged; please open an issue to discuss feature ideas first.

For detailed information on how to contribute, see [here](/CONTRIBUTING.md).

## 📃 License

Chainnext is a fork of Chainlit and is open-source under the [Apache 2.0](LICENSE) license.
