from __future__ import annotations

import configparser
import json
import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


def main() -> int:
    """Read version from pyproject.toml, then package.json, then setup.cfg."""
    version: str | None = None

    if (path_pyproject := Path("pyproject.toml")).is_file():
        with open(path_pyproject, "rb") as fp:
            data = tomllib.load(fp)

        try:
            version = data["project"]["version"]
        except KeyError:
            pass

    if version is None and (path_pkg := Path("package.json")).is_file():
        with open(path_pkg, encoding="utf-8") as fp:
            data = json.load(fp)
        v = data.get("version")
        if isinstance(v, str) and v.strip():
            version = v.strip()

    if version is None and (path_setup_cfg := Path("setup.cfg")).is_file():
        parser = configparser.ConfigParser()
        parser.read(path_setup_cfg)

        try:
           version = parser["metadata"]["version"]
        except KeyError:
            pass

    if version is None:
       return 1
    print(version)
    return 0


if __name__ == "__main__":
    sys.exit(main())
