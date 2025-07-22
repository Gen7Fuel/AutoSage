import streamlit as st
from streamlit.logger import get_logger

# Landing page
import landing

LOGGER = get_logger(__name__)
st.set_page_config(
    page_title="Gen7Fuel: Doc Formatter",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

def run():
    landing.main()

def startup():
    run()

if __name__ == "__main__":
    startup()