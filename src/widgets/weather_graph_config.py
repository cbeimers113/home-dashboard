import urllib
from typing import Any, Optional

import dash_daq as daq
import requests
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from meteostat import Point
from requests.exceptions import RequestException

import src.model as Model
from .ids import WOP_CONTAINER_ID, WOP_GET_BUTTON_ID, WOP_N_DAYS_ID, WOP_N_MONTHS_ID, WOP_SEARCH_INPUT_ID, VOID


def load_location(search_name: str) -> None:
    """Load the location object from Openstreetmap from a given search term."""
    try:
        # Extract the position on Earth's surface and the formal name of the location
        url = f'https://nominatim.openstreetmap.org/search/{urllib.parse.quote(search_name)}?format=json'
        response: dict[str: Any] = requests.get(url).json()[0]

        Model.LOC_FULL_NAME = response['display_name']
        Model.LOC_SHORT_NAME = extract_location_short_name(response['display_name'])
        Model.LOC_POINT = Point(
            float(response['lat']),
            float(response['lon'])
        )
        Model.LOC_LOAD_EXCEPTION = None
    except RequestException as ex:
        # Overwrite location data as null, store the exception
        Model.LOC_FULL_NAME = None
        Model.LOC_SHORT_NAME = None
        Model.LOC_POINT = None
        Model.LOC_LOAD_EXCEPTION = ex


def extract_location_short_name(full_name: str) -> str:
    """Get the shortened name of a location from the full name."""
    name_tokens = full_name.split(',')
    city = name_tokens[0].strip()
    country = name_tokens[-1].strip()

    # Scan backwards for the province/territory/state. It's usually the one before the postal code (if there is one) or country
    region_index = -2
    while any(c.isdigit() for c in name_tokens[region_index]):
        region_index -= 1
    region = name_tokens[region_index].strip()

    return f'{city}, ' + (f'{region}, ' if region != city else '') + country


def is_location_loaded() -> bool:
    """Return whether a location has been loaded to the state."""
    return Model.LOC_POINT is not None


def get_location_load_exception() -> Optional[RequestException]:
    """Return the location load exception if there was one."""
    return Model.LOC_LOAD_EXCEPTION


def render(app: Dash) -> html.Div:
    """Render the location search box."""
    @app.callback(
        Output(component_id=WOP_SEARCH_INPUT_ID, component_property='value'),
        Input(component_id=WOP_GET_BUTTON_ID, component_property='n_clicks'),
        State(component_id=WOP_SEARCH_INPUT_ID, component_property='value')
    )
    def load_location_callback(_: int, search_name: str) -> str:
        """Tell the backend to load a location into the model."""
        if search_name is not None and len(search_name):
            load_location(search_name)

        return ''

    @app.callback(
        Output(component_id=VOID(), component_property='value'),
        Input(component_id=WOP_N_MONTHS_ID, component_property='value')
    )
    def set_n_months(n_months: int) -> None:
        """Read the n_months counter and assign it to the model."""
        Model.WGR_N_MONTHS = n_months

    @app.callback(
        Output(component_id=VOID(), component_property='value'),
        Input(component_id=WOP_N_DAYS_ID, component_property='value')
    )
    def set_n_days(n_days: int) -> None:
        """Read the n_days counter and assign it to the model."""
        Model.WGR_N_DAYS = n_days

    return html.Div(
        className=WOP_CONTAINER_ID,
        children=[
            html.H4('Search for a location to report:'),
            html.Br(),
            dcc.Input(
                id=WOP_SEARCH_INPUT_ID,
                type='text'
            ),
            html.Button(
                id=WOP_GET_BUTTON_ID,
                type='submit',
                children='Submit',
                style={
                    'margin-left': '20px'
                }
            ),
            html.Hr(),
            daq.NumericInput(
                id=WOP_N_DAYS_ID,
                value=3,
                min=1,
                max=30,  # 1 month
                label='Weather for the past n days:',
                labelPosition='top'
            ),
            html.Br(),
            daq.NumericInput(
                id=WOP_N_MONTHS_ID,
                value=3,
                min=1,
                max=12 * 5,  # 5 years
                label='Weather for the past n months:',
                labelPosition='top'
            ),
        ]
    )
