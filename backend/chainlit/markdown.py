import os
from pathlib import Path

from chainlit.logger import logger

from ._utils import is_path_inside

# Default chainlit.md file created if none exists
DEFAULT_MARKDOWN_STR = """# Welcome to Chainnext! 🚀🤖

Hi there, Developer! 👋 We're excited to have you on board. Chainnext is a Chainlit-compatible framework for prototyping, debugging, and sharing applications built on top of LLMs.

Install the PyPI package with `pip install chainnext`. In your code, keep using `import chainlit` and the `chainlit` CLI — those names are unchanged for compatibility.

## Useful Links 🔗

- **Repository:** [chainnext on GitHub](https://github.com/Puyanfar/chainnext) 📦
- **Documentation:** Upstream Chainlit API docs still apply: [Chainlit Documentation](https://docs.chainlit.io) 📚

We can't wait to see what you create with Chainnext! Happy coding! 💻😊

## Welcome screen

To modify the welcome screen, edit the `chainlit.md` file at the root of your project. If you do not want a welcome screen, just leave this file empty.
"""


def init_markdown(root: str):
    """Initialize the chainlit.md file if it doesn't exist."""
    chainlit_md_file = os.path.join(root, "chainlit.md")

    if not os.path.exists(chainlit_md_file):
        with open(chainlit_md_file, "w", encoding="utf-8") as f:
            f.write(DEFAULT_MARKDOWN_STR)
            logger.info(f"Created default chainlit markdown file at {chainlit_md_file}")


def get_markdown_str(root: str, language: str) -> str | None:
    """Get the chainlit.md file as a string."""
    root_path = Path(root)
    translated_chainlit_md_path = root_path / f"chainlit_{language}.md"
    default_chainlit_md_path = root_path / "chainlit.md"

    if (
        is_path_inside(translated_chainlit_md_path, root_path)
        and translated_chainlit_md_path.is_file()
    ):
        chainlit_md_path = translated_chainlit_md_path
    else:
        chainlit_md_path = default_chainlit_md_path
        logger.warning(
            f"Translated markdown file for {language} not found. Defaulting to chainlit.md."
        )

    if chainlit_md_path.is_file():
        return chainlit_md_path.read_text(encoding="utf-8")
    else:
        return None
