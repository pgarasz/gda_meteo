from sqlalchemy import Column, Float, DateTime, SmallInteger
from sqlalchemy.orm import declarative_base


Base = declarative_base()


def build_outpost_table(outpost_code):
    """Return outpost table mapping class with parametized tablename."""

    class Outpost(Base):

        __tablename__ = f'outpost_{outpost_code}'

        datetime = Column(DateTime, primary_key=True)
        rain = Column(Float(1), nullable=True)
        water = Column(Float(1), nullable=True)
        flow = Column(Float(1), nullable=True)
        winddir = Column(SmallInteger, nullable=True)
        windlevel = Column(Float(1), nullable=True)
        temp = Column(Float(1), nullable=True)
        pressure = Column(Float(1), nullable=True)
        humidity = Column(Float(1), nullable=True)
        sun = Column(Float(1), nullable=True)

    return Outpost
