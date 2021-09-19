from sqlalchemy import Column, Float, DateTime, SmallInteger, String, Integer
from sqlalchemy.orm import declarative_base


Base = declarative_base()


def build_outpost_table(outpost_code):
    """Return outpost table mapping class with parametized tablename."""

    class Outpost(Base):

        __tablename__ = f'outpost_{outpost_code}'

        datetime = Column(DateTime, primary_key=True)
        wind_dir = Column(SmallInteger)
        wind_speed = Column(Float(1))

    return Outpost
