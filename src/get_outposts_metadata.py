from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from common.utils import Config
from common.base import GdaMeteo
from db.schema import OutpostsMetadata


conf = Config('config.json')

gda_meteo = GdaMeteo(conf.api_key)
engine = create_engine(conf.db_url, echo=False, future=True)

table = OutpostsMetadata

table.__table__.drop(engine)
table.__table__.create(engine, checkfirst=True)


print("Connecting with gdanskiewody.pl ...")

with Session(engine, future=True) as session:

    outposts = gda_meteo.get_outposts_list()

    for metadata in outposts:
        session.add(table(**metadata))

    session.commit()

print("Outposts metadata downloaded to database")
