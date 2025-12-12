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

    # Dart: generate embedded data file
    generate_dart_data()

    # Copy LICENSE to both packages
    license_src = ROOT / "LICENSE"
    shutil.copy(license_src, JS_DIR / "LICENSE")
    shutil.copy(license_src, DART_DIR / "LICENSE")


def generate_dart_data():
    """Generate Dart data file with embedded JSON."""
    dart_template_file = DART_DIR / "lib" / "src" / "data.template.dart"
    dart_out_file = DART_DIR / "lib" / "src" / "data.dart"
    
    # Ensure template exists
    if not dart_template_file.exists():
        raise FileNotFoundError(
            f"Template file not found: {dart_template_file}\n"
            "Make sure packages/dart/lib/src/data.template.dart exists with placeholders."
        )
    
    # Read JSON files
    nodes_json = (DATA_SRC / "nodes.json").read_text()
    edges_json = (DATA_SRC / "edges.json").read_text()
    meta_json = (DATA_SRC / "meta.json").read_text()
    
    # Read template
    template = dart_template_file.read_text()

    # Ensure placeholders exist (avoid silently generating stale output)
    required_placeholders = [
        "__NODES_JSON_PLACEHOLDER__",
        "__EDGES_JSON_PLACEHOLDER__",
        "__META_JSON_PLACEHOLDER__",
    ]
    missing = [p for p in required_placeholders if p not in template]
    if missing:
        raise ValueError(
            f"Missing placeholders in {dart_template_file}: {', '.join(missing)}"
        )
    
    # Replace placeholders
    template = template.replace("__NODES_JSON_PLACEHOLDER__", nodes_json)
    template = template.replace("__EDGES_JSON_PLACEHOLDER__", edges_json)
    template = template.replace("__META_JSON_PLACEHOLDER__", meta_json)
    
    # Verify all placeholders were replaced
    if "__NODES_JSON_PLACEHOLDER__" in template:
        raise ValueError("Failed to replace __NODES_JSON_PLACEHOLDER__")
    if "__EDGES_JSON_PLACEHOLDER__" in template:
        raise ValueError("Failed to replace __EDGES_JSON_PLACEHOLDER__")
    if "__META_JSON_PLACEHOLDER__" in template:
        raise ValueError("Failed to replace __META_JSON_PLACEHOLDER__")
    
    # Write generated file
    dart_out_file.write_text(template)
    print(f"Generated {dart_out_file}")


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

