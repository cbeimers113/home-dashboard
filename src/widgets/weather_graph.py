from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Optional, Union

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from meteostat import Daily, Hourly

import src.model as Model
from .ids import POLL_ID, WGR_CONTAINER_ID, WGR_GRAPH_CONTAINER_ID, WOP_N_DAYS_ID, WOP_N_MONTHS_ID
from .weather_graph_config import get_location_load_exception, is_location_loaded


# TODO: Add weather analytics (see scikit-learn and Prophet)


def get_hourly_weather_data() -> Optional[pd.DataFrame]:
    """Retrieve the hourly weather data from start_date to today."""
    if not is_location_loaded():
        return None

    start_date = datetime.today() - relativedelta(days=Model.WGR_N_DAYS)
    return Hourly(Model.LOC_POINT, start_date, datetime.today()).fetch()


def get_daily_weather_data() -> Optional[pd.DataFrame]:
    """Retrieve the daily weather data from start_date to today."""
    if not is_location_loaded():
        return None

    start_date = datetime.today() - relativedelta(months=Model.WGR_N_MONTHS)
    return Daily(Model.LOC_POINT, start_date, datetime.today()).fetch()


def render(app: Dash) -> Union[html.Div, dcc.Graph]:
    """Render the weather data for a selected date range and location."""
    @app.callback(
        Output(component_id=WGR_GRAPH_CONTAINER_ID, component_property='children'),
        Input(component_id=POLL_ID, component_property='n_intervals'),
        State(component_id=WOP_N_DAYS_ID, component_property='value'),
        State(component_id=WOP_N_MONTHS_ID, component_property='value')
    )
    def refresh_graphs(_: int, n_days: int, n_months: int) -> Optional[html.Div]:
        """Refresh the weather history graph."""
        if not is_location_loaded():
            # If there is no state loaded, report any exceptions that may have arisen
            return html.Div(html.H4(get_location_load_exception() or 'Enter your Location →'))

        hourly_data = get_hourly_weather_data()
        daily_data = get_daily_weather_data()

        return html.Div(children=[
            html.H4(f'Weather History for {Model.LOC_SHORT_NAME}'),
            # TODO: Make graphs fit better on page
            # TODO: Axis labels and other graph features
            dcc.Graph(
                figure=px.scatter(
                    title=f'Hourly Average Temperature for Past {Model.WGR_N_DAYS} Days',
                    x=hourly_data.index,
                    y=hourly_data['temp']
                )
            ),
            html.Br(),
            dcc.Graph(
                figure=px.scatter(
                    title=f'Daily Average Temperatue for Past {Model.WGR_N_MONTHS} Months',
                    x=daily_data.index,
                    y=daily_data['tavg']
                )
            )
        ])

    return html.Div(
        className=WGR_CONTAINER_ID,
        children=html.Div(id=WGR_GRAPH_CONTAINER_ID)
    )
