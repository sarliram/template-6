import importlib
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from database import Base, engine

FEATURE_DIR = Path(__file__).parent / "feature"

mcp = FastMCP("app", stateless_http=True)


def register_feature_tools(server: FastMCP):
    for tools_file in sorted(FEATURE_DIR.glob("*/tools.py")):
        tools_module = importlib.import_module(f"feature.{tools_file.parent.name}.tools")
        for tool in getattr(tools_module, "tools", []):
            server.add_tool(tool)


register_feature_tools(mcp)

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    mcp.run()
