from sqlalchemy import MetaData
from sqlalchemy_utils import create_view

from db.schema import build_outpost_table
from db.statistics import monthly_avg_rainfall, monthly_avg_temp, wind_rose


def _create_outpost_stats_view(outpost_number,
                               engine,
                               stats_func,
                               refresh):

    view_name = f'o{outpost_number}_{stats_func.__name__}'
    metadata = MetaData()
    table = build_outpost_table(str(outpost_number))
    query = stats_func(table)

    create_view(view_name, query, metadata,
                cascade_on_drop=False)

    if refresh:
        metadata.drop_all(engine)

    metadata.create_all(engine)


def create_view_monthly_avg_rainfall(outpost_number, engine, refresh=True):

    _create_outpost_stats_view(outpost_number, engine,
                               stats_func=monthly_avg_rainfall,
                               refresh=refresh)


def create_view_monthly_avg_temp(outpost_number, engine, refresh=True):

    _create_outpost_stats_view(outpost_number, engine,
                               stats_func=monthly_avg_temp,
                               refresh=refresh)


def create_view_wind_rose(outpost_number, engine, refresh=True):

    _create_outpost_stats_view(outpost_number, engine,
                               stats_func=wind_rose,
                               refresh=refresh)
