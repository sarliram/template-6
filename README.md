# FastAPI Project

This is a FastAPI project with SQLAlchemy for database interaction

## Prerequisites

Before you begin, make sure you have the following installed:

- [uv](https://docs.astral.sh/uv/) (Python package and project manager; it installs Python 3.12 for you if needed)

## Setting Up the Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/your-fastapi-project.git
   cd your-fastapi-project
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```
   This creates `.venv` and installs the exact versions pinned in `uv.lock`.

3. **Configure the environment:**
   ```bash
   cp .env.example .env
   ```
   Then set `DATABASE_URL` in `.env` to your MySQL connection string, and `PORT` for the API server (default: `8000`). `.env` is git-ignored, so credentials stay out of the repository.

4. **Run the API:**
   ```bash
   uv run main.py
   ```
   This starts uvicorn with auto-reload on the `PORT` from `.env`.

### Managing dependencies

- Add a package: `uv add <package>`
- Remove a package: `uv remove <package>`
- Dependencies are declared in `pyproject.toml` and locked in `uv.lock`; commit both.

## MCP Server

Feature endpoints are also exposed as MCP tools so AI agents can use them. `mcp_server.py` finds every `feature/<name>/tools.py` and registers the functions listed in its `tools` list.

- **Local (stdio):** `uv run mcp_server.py`, used by Claude Code / Claude Desktop / Cursor.
- **Web (HTTP):** served by the API itself at `http://127.0.0.1:<PORT>/mcp` while `uv run main.py` is running. For web-based agents, expose it with a tunnel, e.g. `cloudflared tunnel --url http://localhost:<PORT>`, and use `https://<tunnel-host>/mcp`.
  > ⚠️ The HTTP endpoint has **no authentication**. Anyone with the URL can create, edit and delete data. Only expose it temporarily for testing.
- Claude Code picks it up automatically from `.mcp.json` when opened in this folder.
- Other clients (e.g. Claude Desktop) can use the same config:
  ```json
  { "mcpServers": { "app": { "command": "uv", "args": ["run", "--directory", "/absolute/path/to/project", "mcp_server.py"] } } }
  ```

### Adding MCP tools for a new feature

Create `feature/<name>/tools.py` next to its `routes.py`, write each tool as a typed function with a docstring (the docstring becomes the tool description), and list them at the bottom:

```python
tools = [create_product, list_products, get_product]
```

No changes to `mcp_server.py` are needed. Current todo tools: `create_todo`, `list_todos`, `list_todos_paginated`, `get_todo`, `update_todo`, `delete_todo`.
