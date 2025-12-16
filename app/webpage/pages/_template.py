import streamlit as st

def render():
    """Template for new pages.

    Create a new file under `app/webpage/pages/your_page.py` and copy this
    `render()` skeleton. The dynamic loader in `app/webpage/web.py` will
    discover it automatically (module name must not start with `_`).
    """
    st.header("New Page")
    st.write("Replace this content with your page implementation.")


if __name__ == "__main__":
    render()
