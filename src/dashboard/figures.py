import pandas as pd
import plotly.express as px
import plotly.io as pio

from common import conf
from db.views import create_view_monthly_avg_temp, create_view_monthly_avg_rainfall, create_view_wind_rose

pio.templates.default = conf.plotly_theme


def plot_monthly_avg_rainfall(outpost_code, engine):

    name = f"o{outpost_code}_monthly_avg_rainfall"

    try:
        df = pd.read_sql_table(name, engine)
    except ValueError:
        create_view_monthly_avg_rainfall(outpost_code, engine)
        df = pd.read_sql_table(name, engine)

    fig = px.bar(df, x='month', y='rainfall_sum',
                 labels={'rainfall_sum': '[mm]',
                         'month': 'month'},)

    fig.update_layout(
        title='Monthly Avarage Rainfall',
        xaxis=dict(type='category', title='')
    )

    return fig


def plot_monthly_avg_temp(outpost_code, engine):

    name = f"o{outpost_code}_monthly_avg_temp"

    try:
        df = pd.read_sql_table(name, engine)
    except ValueError:
        create_view_monthly_avg_temp(outpost_code, engine)
        df = pd.read_sql_table(name, engine)

    fig = px.bar(df, x='month', y='avg_temp',
                 color='avg_temp',
                 labels={'avg_temp': '[\u00B0C]',
                         'month': 'month'},
                 color_continuous_scale='Portland',
                 range_color=[-10, 30],)

    fig.update_layout(
        title='Monthly Avarage Temperature',
        xaxis=dict(type='category', title=''),
    )
    fig.update_coloraxes(showscale=False)

    return fig


def plot_wind_rose(outpost_code, engine):

    name = f"o{outpost_code}_wind_rose"

    try:
        df = pd.read_sql_table(name, engine)
    except ValueError:
        create_view_wind_rose(outpost_code, engine)
        df = pd.read_sql_table(name, engine)

    fig = px.bar_polar(df, r="frequency", theta="direction", color="strength",
                       color_discrete_sequence=px.colors.sequential.deep,
                       category_orders={'direction': ['N', 'NNE', 'NE', 'ENE',
                                                      'E', 'ESE', 'SE', 'SSE',
                                                      'S', 'SSW', 'SW', 'WSW',
                                                      'W', 'WNW', 'NW', 'NNW'],
                                        'strength': ['c', '0-1', '1-3',
                                                     '3-5', '5-8', '8-11',
                                                     '11-18', '18-30', '>=30']
                                        }
                       )

    fig.update_layout(
        title='Wind Speed Distribution',
        polar_radialaxis_ticksuffix='%',
        legend_title='[m/s]',
    )

    return fig
