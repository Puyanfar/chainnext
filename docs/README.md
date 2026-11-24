# Documentation for Chainnext developers, contributors, and AI coding assistants.

Chainnext is published on PyPI as **`chainnext`**. Application code still uses
**`import chainlit`** and the **`chainlit`** CLI. See
[Names: PyPI vs import vs CLI](../README.md#names-pypi-vs-import-vs-cli).

See also:

- [CONTRIBUTING.md](../CONTRIBUTING.md) — contribution guidelines
- [CHANGELOG.md](../CHANGELOG.md) — release history
- [Semantic Kernel integration status](semantic-kernel.md)
- [MCP security advisory](security-advisory-2026-mcp.md)
- [Context7 library IDs](context7.md)

## Research

Internal notes on CI, tooling, and test layout. These are historical snapshots
unless a status note says otherwise; check the current workflows before following
them.

- [CI cache optimization](research/ci-cache-optimization.md)
- [Copilot type-checking](research/copilot-type-checking.md)
- [E2E parallel execution](research/e2e-parallel-execution.md)

## Plans

Historical implementation plans:

- [ESLint v9 migration](plans/2026-03-31-eslint-v9-migration.md)
- [CI cache P2: react-client build cache](plans/2026-04-06-ci-cache-p2-react-client-build-cache.md)
