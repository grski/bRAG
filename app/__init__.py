import tomllib
from pathlib import Path

with Path.open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)
    version = data["project"]["version"]
