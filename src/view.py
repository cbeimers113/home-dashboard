import dash_bootstrap_components as dbc
from dash import Dash, dcc, html

import src.widgets.weather_graph as WeatherGraph
import src.widgets.weather_graph_config as WeatherGraphConfig
from .widgets.ids import placeholder_ids, MAIN_APP_ID, POLL_ID


def create_layout(app: Dash) -> html.Div:
    """Create the dashboard layout."""
    return html.Div(
        className=MAIN_APP_ID,
        children=[
            html.Center(html.H1(app.title)),
            html.Hr(),
            # Each widget gets its own card and grid cell
            # TODO: fancify cards
            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            WeatherGraph.render(app)
                        ])
                    ),
                    width=9
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            WeatherGraphConfig.render(app)
                        ])
                    ),
                    width=3
                )
            ]),
            # TODO: Add network status widget

            # Add a polling event every second
            dcc.Interval(id=POLL_ID, interval=1000, n_intervals=0),

            # Add the placeholder ids and make them hidden
            html.Div(children=[html.P(id=_id) for _id in placeholder_ids]),
            # style={‘display’:‘none’}
        ],
        style={
            'padding-top': '10px',
            'padding-left': '10px',
            'padding-bottom': '10px',
            'padding-right': '10px',
            'font-family': 'Ubuntu'
        }
    )
