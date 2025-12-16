import streamlit as st
import importlib
import pkgutil
import inspect
from pathlib import Path

st.set_page_config(page_title="Industrial AI Platform", layout="wide")

PAGES_PKG = "app.webpage.pages"
PAGES_DIR = Path(__file__).parent / "pages"


def discover_pages():
    pages = []
    for finder, name, ispkg in pkgutil.iter_modules([str(PAGES_DIR)]):
        if name.startswith("_"):
            continue
        pages.append(name)
    pages.sort()
    return pages


def render_page(page_name: str):
    module_name = f"{PAGES_PKG}.{page_name}"
    try:
        # always import fresh to reflect changes during development
        if module_name in globals():
            importlib.reload(globals()[module_name])
        module = importlib.import_module(module_name)
        globals()[module_name] = module
    except Exception as e:
        st.error(f"Failed to load page '{page_name}': {e}")
        return

    # If the module exposes a `render()` function call it, otherwise the
    # module will execute top-level Streamlit code on import (legacy pages).
    if hasattr(module, "render") and inspect.isfunction(module.render):
        module.render()


def main():
    st.sidebar.title("Navigation")
    pages = discover_pages()
    display_names = [p.replace("_", " ").title() for p in pages]
    selected = st.sidebar.selectbox("Pages", display_names)
    page_idx = display_names.index(selected)
    page_name = pages[page_idx]

    st.title("Industrial AI Platform")
    st.markdown(
        """
        Welcome — use the sidebar to navigate pages. Add new pages by creating
        a Python file under `app/webpage/pages/` (module must not start with `_`).
        If your page defines a `render()` function it will be called, otherwise
        top-level Streamlit code in the module will run on import.
        """
    )

    render_page(page_name)


if __name__ == "__main__":
    main()
