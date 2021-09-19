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

gda_meteo = GdaMeteo(api_key)
table = build_outpost_table(outpost_code)
engine = create_engine('sqlite:///../db/gda_meteo.db', echo=False, future=True)

table.__table__.create(bind=engine, checkfirst=True)

print_start_info(outpost_code, start_date, end_date)

with Session(engine) as session:

    for date in dates_generator(start_date, end_date):

        wind_dir = gda_meteo.get_winddir(date, outpost_code)
        wind_speed = gda_meteo.get_windspeed(date, outpost_code)

        print(f'   {date}')

        zipped = zip(wind_dir, wind_speed)                 # API zawsze zwraca 24 wartości dla dnia
        hourly = {d[0]: [d[1], s[1]] for d, s in zipped}   # {datatime: [direction, speed]}

        for h, v in hourly.items():
            row = table(datetime=datetime.fromisoformat(h),
                        wind_dir=v[0], wind_speed=v[1])
            session.add(row)

    session.commit()
