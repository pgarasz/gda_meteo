from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from common.utils import get_api_key, dates_generator, print_start_info
from common.base import GdaMeteo
from db.schema import build_outpost_table


api_key = get_api_key('config.json')

start_date = '2017-09-06'
end_date = '2017-09-11'
outpost_code = 31
params = ['rain', 'winddir', 'windlevel', 'temp', 'pressure', 'humidity']

gda_meteo = GdaMeteo(api_key)
table = build_outpost_table(outpost_code)
engine = create_engine('sqlite:///../db/gda_meteo.db', echo=False, future=True)

table.__table__.create(bind=engine, checkfirst=True)

print_start_info(outpost_code, start_date, end_date)

with Session(engine) as session:

    for date in dates_generator(start_date, end_date):

        print(f'   {date}')

        hourly_data = gda_meteo.get_meteo_params(date, outpost_code, params)

        for dt in hourly_data:
            row = table(datetime=datetime.fromisoformat(dt), **hourly_data[dt])
            session.add(row)

        session.commit()
