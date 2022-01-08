from collections import namedtuple
import re

from sqlalchemy import inspect, select, String, cast
from sqlalchemy.orm import Session

from db.schema import OutpostsMetadata

OutpostInfo = namedtuple("OutpostInfo", ['id', 'name', 'table_name'])


class DBInfo:

    def __init__(self, engine):
        self.engine = engine
        self.table_names = inspect(engine).get_table_names()
        self.outposts_metadata = self._get_outposts_metadata()

    def _get_outposts_metadata(self):

        result = {}
        query = select(
            cast(OutpostsMetadata.no, String),
            OutpostsMetadata
        )

        with Session(self.engine) as session:
            for no, row in session.execute(query):
                result[no] = row

        return result

    def get_outpost_name(self, no):
        return self.outposts_metadata[str(no)].name

    @property
    def outpost_table_names(self):
        regex = re.compile(r"(?<=outpost_)\d+")

        return [n for n in self.table_names if regex.search(n)]

    @property
    def outpost_ids(self):
        return [n.split("_")[1] for n in self.outpost_table_names]

    @property
    def outposts(self) -> list[OutpostInfo]:

        meta = self.outposts_metadata
        outposts = []

        for id in self.outpost_ids:
            outposts.append(
                OutpostInfo(id, meta[id].name, f"outpost_{id}")
            )

        return outposts

# TODO min i max datetime?
