# local imports
import src.demand_analysis_assistant.app as demand_analysis_assistant
# import utils.layout as layout
# from utils import analytics, analytics_events

# analytics.track_event(analytics_events.EXPERIMENT_ANALYSIS_CLICK)

# calling app wise layout
# layout.wide()


from utils.security import require_login
require_login()

demand_analysis_assistant.run()
