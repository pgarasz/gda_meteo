import dash_bootstrap_components as dbc

from dash import Dash

app = Dash(name=__name__,
           external_stylesheets=[dbc.themes.FLATLY],
           suppress_callback_exceptions=True,
           )

app.title = "Gdańsk Meteo"
