from argparse import ArgumentParser
from datetime import datetime, date as dtdate

from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session

from common.utils import Config, dates_generator, print_start_info
from common.base import GdaMeteo, DEFAULT_METEO_PARAMS
from db.schema import build_outpost_table


parser = ArgumentParser(prog='GdaMeteo data downloader',
                        description='Download meteo data from gdanskiewody.pl to database')

parser.add_argument('start_date', type=dtdate.fromisoformat,
                    help="Input start date in iso format YYYY-MM-DD")
parser.add_argument('end_date', type=dtdate.fromisoformat,
                    help="Input end date in iso format YYYY-MM-DD")
parser.add_argument('outpost_code', type=int)
parser.add_argument('--params', nargs='?', dest='params',
                    default=DEFAULT_METEO_PARAMS,
                    help="Choose meteo parameters to be downloaded for the selected outpost.     \
                          Eg. temp rain. By default all standard parameters are downloaded       \
                          -> (%s)" % ' '.join(DEFAULT_METEO_PARAMS)
                    )
parser.add_argument('-w', '--overwrite', action='store_true',
                    dest='overwrite', default=False,
                    help="Overwrites entries in the database")

args = parser.parse_args()

start_date = args.start_date
end_date = args.end_date
outpost_code = args.outpost_code
params = args.params
overwrite = args.overwrite

conf = Config('config.json')

gda_meteo = GdaMeteo(conf.api_key)
table = build_outpost_table(outpost_code)
engine = create_engine(conf.db_url, echo=False, future=True)

table.__table__.create(bind=engine, checkfirst=True)

print_start_info(outpost_code, start_date, end_date)

with Session(engine, future=True) as session:

    existing_dates = session.execute(select(table.datetime)).scalars().all()

    for date in dates_generator(start_date, end_date):

        if not overwrite and datetime.fromisoformat(date) in existing_dates:
            print(f'   {date} - already in database')
            continue

        print(f'   {date}')
        hourly_data = gda_meteo.get_meteo_params(date, outpost_code, params)

        for dt in hourly_data:

            if overwrite and datetime.fromisoformat(dt) in existing_dates:
                stmt = update(table)                                                \
                    .where(table.datetime == dt)                                    \
                    .values(**hourly_data[dt])
                session.execute(stmt)
            else:
                row = table(datetime=datetime.fromisoformat(dt), **hourly_data[dt])
                session.add(row)

        session.commit()
