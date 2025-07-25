# local imports
import src.canco_price_importer.app as canco_price_importer
# import utils.layout as layout
# from utils import analytics, analytics_events

# analytics.track_event(analytics_events.EXPERIMENT_ANALYSIS_CLICK)

# calling app wise layout
# layout.wide()

from utils.security import require_login
require_login()

canco_price_importer.run()
