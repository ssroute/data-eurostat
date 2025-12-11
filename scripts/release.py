#!/usr/bin/env python3
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_SRC = ROOT / "data"
JS_DIR = ROOT / "packages" / "js"
DART_DIR = ROOT / "packages" / "dart"


def get_version() -> str:
    return (ROOT / "VERSION").read_text().strip()


def sync_data():
    # JS: copy data -> js/data
    js_data = JS_DIR / "data"
    if js_data.exists():
        shutil.rmtree(js_data)
    shutil.copytree(DATA_SRC, js_data)

    # Dart: copy data -> dart/lib/src/data
    dart_data = DART_DIR / "lib" / "src" / "data"
    if dart_data.exists():
        shutil.rmtree(dart_data)
    dart_data.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(DATA_SRC, dart_data)

    # Copy LICENSE to both packages
    license_src = ROOT / "LICENSE"
    shutil.copy(license_src, JS_DIR / "LICENSE")
    shutil.copy(license_src, DART_DIR / "LICENSE")


def sync_versions(version: str):
    # packages/js/package.json
    pkg_path = JS_DIR / "package.json"
    pkg = json.loads(pkg_path.read_text())
    pkg["version"] = version
    pkg_path.write_text(json.dumps(pkg, indent=2) + "\n")

    # dart/pubspec.yaml (simple line replace for 'version:')
    pubspec_path = DART_DIR / "pubspec.yaml"
    lines = []
    for line in pubspec_path.read_text().splitlines():
        if line.startswith("version:"):
            lines.append(f"version: {version}")
        else:
            lines.append(line)
    pubspec_path.write_text("\n".join(lines) + "\n")


def main():
    version = get_version()
    print(f"Preparing release v{version}")
    sync_data()
    sync_versions(version)
    print("Data and versions synced.")
    print("Next steps:")
    print("  cd packages/js && npm publish --access public")
    print("  cd packages/dart && dart pub publish")
    print(f"  git tag v{version} && git push && git push --tags")


if __name__ == "__main__":
    main()

