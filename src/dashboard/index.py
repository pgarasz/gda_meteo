import dash_bootstrap_components as dbc

from dash import html, dcc

from dashboard import app
from dashboard.elements import navbar
from dashboard.callbacks import render_page_content, get_outpost_figures_left_col, \
                          get_outpost_figures_right_col

from db import connect_engine
from db.utils import DBInfo

engine = connect_engine()
db_info = DBInfo(engine)


app.layout = html.Div([
    dcc.Location(id="url"),
    navbar("Gdańsk Meteo", db_info.outposts),
    html.Br(),
    dbc.Container(id="content")
])
