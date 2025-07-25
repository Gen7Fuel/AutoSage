import streamlit as st

AUTHORIZED_USERS = {
    "peter": "gen7secure",
    "admin": "admin123",
}

def require_login():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.title("🔐 Gen7Fuel: AutoSage Login")
        st.markdown("Please login to continue.")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username in AUTHORIZED_USERS and AUTHORIZED_USERS[username] == password:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ Invalid username or password.")
        st.stop()  # Prevent rest of app from loading
