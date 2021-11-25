def connect_engine(echo: bool = False, future: bool = False):
    "Convenience function for connecting with the database"

    from sqlalchemy import create_engine

    from common.utils import Config

    conf = Config('config.json')

    return create_engine(conf.db_url, echo=echo, future=future)
