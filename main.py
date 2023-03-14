import os
import sys

from dash import Dash
from dash_bootstrap_components.themes import SLATE

import src.view as View


def main(debug=False) -> None:
    """The main method."""
    app = Dash(external_stylesheets=[SLATE], update_title=None)
    app.title = 'Home Dashboard'
    app.layout = View.create_layout(app)
    app.run_server(host='0.0.0.0', port=8050)


if __name__ == '__main__':
    main(
        debug=len(sys.argv) > 1 and any(sys.argv[1:]) in ('-d', '--debug'),
    )
