"""Store IDs for view components."""

# Placeholder id generator for when we want a callback with no output
n_placeholders = 0
placeholder_ids = []


def VOID():
    global n_placeholders
    _id = f'null-callback-{n_placeholders}'
    placeholder_ids.append(_id)
    n_placeholders += 1
    return _id


# Interval poll
POLL_ID = 'poll'

# The dashboard
MAIN_APP_ID = 'main-app'

# Weather graph display
WGR_CONTAINER_ID = 'wgr-container'
WGR_GRAPH_CONTAINER_ID = 'wgr-graph-container'

# Weather graph options interface
WOP_CONTAINER_ID = 'wop-container'
WOP_GET_BUTTON_ID = 'wop-get-button'
WOP_N_MONTHS_ID = 'wop-n-months'
WOP_N_DAYS_ID = 'wop-n-days'
WOP_SEARCH_INPUT_ID = 'wop-search-input'
