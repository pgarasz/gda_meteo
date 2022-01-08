import dash_bootstrap_components as dbc

from dash import html, dcc

from dashboard.figures import plot_monthly_avg_rainfall, plot_monthly_avg_temp, plot_wind_rose

from db.utils import OutpostInfo


def get_navbar_items(items: list[OutpostInfo]):
    menu_items = []

    for item in items:
        menu_items.append(
            dbc.DropdownMenuItem(item.name,
                                 id=item.table_name,
                                 href=f"/outpost#{item.id}")
        )

    return menu_items


def navbar(brand: str, outposts: list[OutpostInfo]):

    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Compare", href="/compare")),
            dbc.DropdownMenu(
                children=get_navbar_items(outposts),
                nav=True,
                in_navbar=True,
                label="Outposts",
            ),
        ],
        brand=brand,
        brand_href="/",
        color="primary",
        dark=True,
        fluid=True,
    )

    return navbar


def outpost_figures(outpost_no, outpost_name, engine):
    """Plot figures for outpost and return them as a Bootstrap column"""

    figures = html.Div([

        dbc.Row([
            dbc.Col([
                html.H1(outpost_name),
                html.Br(),
            ]),
        ]),

        dbc.Row([
            dbc.Col(
                dcc.Graph(figure=plot_monthly_avg_temp(outpost_no, engine))
            ),
        ]),
        dbc.Row([
            dbc.Col(
                dcc.Graph(figure=plot_wind_rose(outpost_no, engine))
            ),
        ]),
        dbc.Row([
            dbc.Col(
                dcc.Graph(figure=plot_monthly_avg_rainfall(outpost_no, engine))
            ),
        ]),

        # dbc.Row([
        #     dbc.Col(

        #     ),
        # ]),

    ])

    return figures


def dropdown(element_id: str, items: list[OutpostInfo]):

    options = []

    for item in items:
        options.append(dict(label=item.name, value=item.id))

    dropdown = dcc.Dropdown(
        id=element_id,
        options=options,
        value=None)

    return dropdown


def compare_outposts(items: list[OutpostInfo], engine):

    layout = html.Div([

        dbc.Row([
            dbc.Col([
                dropdown("left_dropdown", items),
                html.Br(),
            ]),
            dbc.Col([
                dropdown("right_dropdown", items),
                html.Br(),
            ]),
        ]),

        dbc.Row([
            dbc.Col(id='left_column'),
            dbc.Col(id='right_column'),
        ]),
    ])

    return layout


def jumbotron(header, main_P, sub_P=''):

    jumbotron = html.Div(
        dbc.Container(
            [
                html.H1(header, className="display-3"),
                html.P(
                    main_P,
                    className="lead",
                ),
                html.Hr(className="my-2"),
                html.P(sub_P),
            ],
            fluid=True,
            className="py-3",
        ),
        className="p-3 bg-light rounded-3",
    )

    return jumbotron


missing_page_error = jumbotron(
    header='Error 404',
    main_P='The page you requested does not exist',
)

welcome_txt = jumbotron(
    header='Welcome!',
    main_P=dcc.Markdown(
        'Welcome to Gdańsk Meteo - a dashboard that shows basic climatological statistics \
         based on data collected by [Gdańskie Wody](http://www.gdmel.pl/) \
         with a network of sensors placed in the  [3City](https://osm.org/go/0PMc4Gb-) metropolitan area.'),
    sub_P=dcc.Markdown(
        'created by [Przemek Garasz](https://www.linkedin.com/in/przemekgarasz/)')
)
