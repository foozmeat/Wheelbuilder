from datetime import datetime
from math import sqrt, sin, pi, cos

from sqlalchemy import MetaData, Column, Integer, String, DateTime, Float, \
    Index
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)

"""
update hubs
set created_on = datetime('now')
where created_on = '0000-00-00 00:00:00'

update hubs
set updated_on = datetime('now')
where updated_on = '0000-00-00 00:00:00'

"""


class Hubs(Base):
    __tablename__ = 'hubs'

    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    s = Column(Float, default=2.5, nullable=False)
    dl = Column(Float, default=0.0, nullable=False)
    dr = Column(Float, default=0.0, nullable=False)
    wl = Column(Float, default=0.0, nullable=False)
    wr = Column(Float, default=0.0, nullable=False)
    old = Column(Float, default=0.0, nullable=False)
    forr = Column(String, default="f", nullable=False)
    comment = Column(String, nullable=True)
    email = Column(String, nullable=True)

    created_on = Column(DateTime, default=datetime.utcnow)
    updated_on = Column(DateTime)

    @property
    def forr_for_display(self):
        return "Front" if self.forr == 'F' else "Rear"

    def __str__(self):
        return f"{self.description} ({self.forr_for_display}"


Index('index_hubs_on_forr', Hubs.forr)
Index('index_hubs_on_description', Hubs.description)


class Rims(Base):
    __tablename__ = 'rims'

    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    erd = Column(Float, default=0.0, nullable=False)
    osb = Column(Float, default=0.0, nullable=False)
    size = Column(Integer, default=0, nullable=False)
    comment = Column(String, nullable=True)
    email = Column(String, nullable=True)

    created_on = Column(DateTime, default=datetime.utcnow)
    updated_on = Column(DateTime)

    @property
    def rim_correction_factor(self):
        rc = {
            0: 0,
            635: 317,
            630: 315,
            622: 315,
            584: 301,
            571: 295,
            559: 300,
            520: 274,
            507: 270,
            451: 245,
            406: 225,
            355: 204,
            349: 200,
            305: 183
        }

        radius = self.erd / 2
        rcf = radius - rc[self.size]
        return round(rcf)

    @property
    def size_for_display(self):
        return rim_sizes.get(self.size, "Unknown")

    def __str__(self):
        return f"{self.description} ({self.size_for_display}"


Index('index_rims_on_size', Rims.size)
Index('index_rims_on_description', Rims.description)


class Wheel:
    def __init__(self, hub, rim, cross=3, spokes=32, nipple_correction=0):
        self.hub = hub
        self.rim = rim
        self.cross = cross
        self.spokes = spokes
        self.nipple_correction = nipple_correction

    @property
    def wl_effective(self):
        return self.hub.wl - self.rim.osb

    @property
    def wr_effective(self):
        return self.hub.wr + self.rim.osb

    @property
    def l_length(self):
        if not self.spokes or not self.hub.dl or not self.rim.erd or not self.cross:
            return 0

        result = sqrt(
            ((self.hub.dl / 2 * sin(2 * pi * self.cross / (self.spokes / 2))) ** 2) +
            ((self.rim.erd / 2 - ((self.hub.dl / 2) * cos(2 * pi * self.cross / (self.spokes / 2)))) ** 2) +
            (self.wl_effective ** 2)
        ) - (self.hub.s / 2) - self.nipple_correction

        return round(result, 1)

    @property
    def r_length(self):
        if not self.spokes or not self.hub.dl or not self.rim.erd or not self.cross:
            return 0

        result = sqrt(
            ((self.hub.dr / 2 * sin(2 * pi * self.cross / (self.spokes / 2))) ** 2) +
            ((self.rim.erd / 2 - ((self.hub.dr / 2) * cos(2 * pi * self.cross / (self.spokes / 2)))) ** 2) +
            (self.wr_effective ** 2)
        ) - (self.hub.s / 2) - self.nipple_correction

        return round(result, 1)


patterns = {
    0: "0-cross (Radial)",
    1: "1-cross",
    2: "2-cross",
    3: "3-cross",
    4: "4-cross",
    5: "5-cross",
}

nipple_corrections = {
    0: "12mm",
    1: "14mm",
    3: "16mm"
}

spoke_counts = [16, 20, 24, 28, 32, 36, 40, 48]

rim_sizes = {
    622: '700C',
    559: '26"',
    584: '650B',
    630: '27"',
    635: '28"',
    571: '650C',
    520: '24"',
    507: '24"',
    451: '20"',
    406: '20"',
    349: '16"',
    305: '16"',
}

if __name__ == '__main__':

    import os
    import importlib
    from sqlalchemy import create_engine

    moa_config = os.environ.get('MOA_CONFIG', 'DevelopmentConfig')
    config = getattr(importlib.import_module('config'), moa_config)

    if "mysql" in config.SQLALCHEMY_DATABASE_URI:
        pass

    engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=True)
    metadata = MetaData(engine, reflect=True)
    print("Creating Tables")

    Base.metadata.create_all(engine)
    # metadata.create_all()
    for t in metadata.tables:
        # t.create()
        print("Table: ", t)
