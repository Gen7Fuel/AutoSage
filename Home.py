import streamlit as st
from utils.security import require_login
from streamlit.logger import get_logger

# Landing page
import landing

LOGGER = get_logger(__name__)
st.set_page_config(
    page_title="Gen7Fuel: AutoSage",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

def run():
    
    require_login()
    landing.main()

def startup():
    # Session-based authentication
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        require_login()
    else:
        run()

if __name__ == "__main__":
    startup()