import subprocess
import sys
import textwrap

import pytest

nest_asyncio2 = pytest.importorskip("nest_asyncio2")

SCRIPT = textwrap.dedent(
    """
    import asyncio
    import os

    import anyio.to_thread

    import chainlit.cli  # applies the nested event loop patch at import time


    async def inner():
        await asyncio.sleep(0)
        return 42


    async def main():
        # Re-entrance, used by chainlit.sync.run_sync and Session.get_config
        assert asyncio.get_event_loop().run_until_complete(inner()) == 42
        # anyio loop detection, used by Starlette's FileResponse / StaticFiles
        await anyio.to_thread.run_sync(os.getpid)


    asyncio.run(main())
    """
)


def test_nested_loop_patch_is_reentrant_and_anyio_compatible():
    result = subprocess.run(
        [sys.executable, "-c", SCRIPT], capture_output=True, text=True, timeout=60
    )
    assert result.returncode == 0, result.stderr


def test_nest_asyncio2_patch_is_anyio_compatible_in_process():
    """Apply nest_asyncio2 in-process and verify asyncio + anyio still cooperate.

    Unlike the subprocess test above, this exercises the patch directly (the same
    ``apply()`` call the CLI makes) so regressions in the patch/anyio interaction
    are caught even if the import-time wiring in ``chainlit.cli`` changes.
    """
    import asyncio

    import anyio
    import sniffio

    nest_asyncio2.apply(
        run_close_loop=True,
        error_on_mispatched=True,
    )

    async def main():
        assert asyncio.current_task() is not None
        assert sniffio.current_async_library() == "asyncio"

        result = await anyio.to_thread.run_sync(lambda: 42)
        assert result == 42

    asyncio.run(main())
