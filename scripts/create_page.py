"""Small helper to scaffold new Streamlit pages under `app/webpage/pages/`.

Usage:
    python scripts/create_page.py my_new_page

This will create `app/webpage/pages/my_new_page.py` with a `render()` skeleton
based on `_template.py`. If the file already exists the script will refuse to
overwrite it unless `--force` is provided.
"""
import sys
from pathlib import Path


PAGES_DIR = Path(__file__).parents[1] / "app" / "webpage" / "pages"
TEMPLATE = PAGES_DIR / "_template.py"


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="page module name (snake_case, no .py)")
    parser.add_argument("--force", action="store_true", help="overwrite if exists")
    args = parser.parse_args()

    name = args.name.strip()
    if not name.isidentifier() or name.startswith("_"):
        print("Invalid page name. Use a valid python identifier and avoid leading underscore.")
        sys.exit(2)

    target = PAGES_DIR / f"{name}.py"
    if target.exists() and not args.force:
        print(f"{target} already exists. Use --force to overwrite.")
        sys.exit(1)

    if not TEMPLATE.exists():
        # fallback minimal skeleton
        content = (
            "import streamlit as st\n\n"
            "def render():\n"
            "    st.header('New Page')\n"
            "    st.write('Add your content here.')\n"
        )
    else:
        content = TEMPLATE.read_text()

    target.write_text(content)
    print(f"Created {target}")


if __name__ == "__main__":
    main()
