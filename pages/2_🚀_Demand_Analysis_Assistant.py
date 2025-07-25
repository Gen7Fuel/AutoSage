# local imports
import src.demand_analysis_assistant.app as demand_analysis_assistant
import streamlit as st
from utils.security import require_login
# import utils.layout as layout
# from utils import analytics, analytics_events

# analytics.track_event(analytics_events.EXPERIMENT_ANALYSIS_CLICK)

# calling app wise layout
# layout.wide()

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    require_login()
else:
    demand_analysis_assistant.run()
