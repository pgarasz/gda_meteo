from datetime import datetime

from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session

from common.utils import Config, dates_generator, print_start_info
from common.base import GdaMeteo
from db.schema import build_outpost_table


conf = Config('config.json')

start_date = '2017-09-06'
end_date = '2017-09-11'
outpost_code = 31
params = ['rain', 'winddir', 'windlevel', 'temp', 'pressure', 'humidity']
overwrite = False

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
