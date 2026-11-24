# Semantic Kernel integration (`cl.SemanticKernelFilter`)

## Status

The Semantic Kernel integration is **present in the source tree but currently disabled**: the
`semantic-kernel` package is **not installed** as a dependency, so the
`cl.SemanticKernelFilter` API is **not usable at this time**.

This is a deliberate, temporary state — not a removal. The integration code is kept intact so it
can be re-enabled with no code changes once a compatible `semantic-kernel` release is available.

## Why it is disabled

The conflict is a **dependency-resolution collision on `pydantic`**, between two hard version
constraints that have no overlapping version:

| Constraint              | Source                                     | Value                                                              |
| ----------------------- | ------------------------------------------ | ------------------------------------------------------------------ |
| Upper bound on pydantic | `semantic-kernel` 1.47.0 (`requires_dist`) | `pydantic>=2.0,<2.14` (with `!=2.10.0,!=2.10.1,!=2.10.2,!=2.10.3`) |
| Lower bound on pydantic | `chainnext` (`backend/pyproject.toml`)     | `pydantic>=2.14.4,<3.0.0`                                          |

`semantic-kernel` 1.47.0 (the latest release at the time of writing) declares:

```
pydantic!=2.10.0,!=2.10.1,!=2.10.2,!=2.10.3,<2.14,>=2.0
```

The `<2.14` upper bound is the problem. Our project requires `pydantic>=2.14.4` (a floor chosen
for the Python 3.15 upgrade and to stay current with pydantic security fixes). A single
`pydantic` version cannot satisfy both `>=2.14.4` and `<2.14`, so **`uv` (and any PEP 508
resolver) cannot find a solution** whenever `semantic-kernel` is part of the dependency graph.
`uv sync` / `uv lock` fails with an unresolvable `pydantic` conflict.

There is no version of `semantic-kernel` that both (a) is the current release line and (b) allows
`pydantic>=2.14.4`. Downgrading our `pydantic` floor to satisfy `semantic-kernel` was rejected
because it would drop us below the pydantic version the rest of the project (and its CVE floor)
relies on.

## What is affected — and what is not

The integration is fully isolated and imported **lazily**, so the impact is narrow:

- **Not affected:** `import chainlit`, the CLI, the server, and every other integration
  (LangChain, LlamaIndex, OpenAI, MistralAI) work exactly as before. Nothing imports
  `semantic_kernel` at package import time.
- **Affected:** only code that actually uses `cl.SemanticKernelFilter`. Accessing it raises
  `ImportError: cannot import name 'SemanticKernelFilter'` (the underlying `semantic_kernel`
  module is not installed).

### Where the integration lives

| File                                           | Lines | Role                                                                                                                                 |
| ---------------------------------------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `backend/chainlit/semantic_kernel/__init__.py` | 9–11  | `TYPE_CHECKING`-only imports of `Kernel`, `FunctionInvocationContext`, `KernelArguments`                                             |
| `backend/chainlit/semantic_kernel/__init__.py` | 14+   | `class SemanticKernelFilter(BaseModel)` — wraps a Semantic Kernel `Kernel` and records each function invocation as a Chainlit `Step` |
| `backend/chainlit/__init__.py`                 | 106   | Lazy (PEP 562 `__getattr__`) import: `from chainlit.semantic_kernel import SemanticKernelFilter`                                     |
| `backend/chainlit/__init__.py`                 | 134   | Lazy-load map entry `"SemanticKernelFilter": "chainlit.semantic_kernel"`                                                             |
| `backend/chainlit/__init__.py`                 | 170   | Listed in the public `__all__`                                                                                                       |

Because the import is lazy (PEP 562) and the `semantic_kernel` imports sit under
`if TYPE_CHECKING:`, removing the package breaks **nothing at import or runtime** — only the
`cl.SemanticKernelFilter` code path.

## For developers who need `cl.SemanticKernelFilter` today

There is no supported configuration that uses both the current `semantic-kernel` and our
`pydantic>=2.14.4` floor. Your options, in order of preference:

1. **Wait for a compatible `semantic-kernel` release** (preferred). See "Re-enabling" below. No
   code changes will be needed on our side.
2. **Install a compatible pair in your own application environment**, accepting that this
   downgrades pydantic below the project floor and may break other dependencies. For example:
   `pip install "semantic-kernel<1.47" "pydantic<2.14"`. This is **not recommended** and is not
   tested or supported by the project.

## Re-enabling the integration

When a `semantic-kernel` release drops the `pydantic<2.14` upper bound (i.e. supports
`pydantic>=2.14.4`):

1. Uncomment the `semantic-kernel` line in the `tests` extra of `backend/pyproject.toml`.
2. Regenerate the lockfile: `uv lock --upgrade` (from the repo root).
3. Verify resolution and run the test suite: `uv sync --all-extras && uv run pytest`.
4. Update this document's status and remove the "disabled" wording.

No changes to `backend/chainlit/semantic_kernel/__init__.py` or `backend/chainlit/__init__.py`
are required — the integration is already wired up.

## Type-checking note

`semantic_kernel.*` is listed in the `[[tool.mypy.overrides]]` `module` array in the root
`pyproject.toml` with `ignore_missing_imports = true`. This is required because the
`TYPE_CHECKING` imports in `backend/chainlit/semantic_kernel/__init__.py` reference a package
that is not installed in the type-checking environment. Keep this override in place while the
integration remains disabled; it has no effect when the package _is_ installed (mypy will use the
real stubs/types).
