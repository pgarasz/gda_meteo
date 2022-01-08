from sqlalchemy import Column, Float, DateTime, SmallInteger, Boolean, Text
from sqlalchemy.orm import declarative_base


Base = declarative_base()


def build_outpost_table(outpost_code):
    """Return outpost table mapping class with parametized tablename."""

    class Outpost(Base):

        __tablename__ = f'outpost_{outpost_code}'
        __table_args__ = {'extend_existing': True}

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


class OutpostsMetadata(Base):

    __tablename__ = 'outposts_metadata'

    no = Column(SmallInteger, primary_key=True)
    name = Column(Text)
    active = Column(Boolean)
    rain = Column(Boolean)
    water = Column(Boolean)
    flow = Column(Boolean)
    winddir = Column(Boolean)
    windlevel = Column(Boolean)
    temp = Column(Boolean)
    pressure = Column(Boolean)
    humidity = Column(Boolean)
    sun = Column(Boolean)
