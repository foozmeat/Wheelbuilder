from datetime import datetime
from math import cos, pi, sin, sqrt

from sqlalchemy import Column, DateTime, Float, Index, Integer, MetaData, String
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

    @property
    def mru_props(self):
        return self.id, self.description

    def as_dict(self):
        return {
            's': self.s,
            'dl': self.dl,
            'dr': self.dr,
            'wl': self.wl,
            'wr': self.wr,
        }


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

    def __init__(self):
        self.rim_size_cache = None

    @property
    def size_for_display(self):
        return rim_sizes_for_display[self.size]

    @property
    def mru_props(self):
        return self.id, self.description

    def as_dict(self):
        return {
            'erd': self.erd,
            'osb': self.osb,
        }

    # def __str__(self):
    #     return f"{self.description} ({self.size_for_display}"


Index('index_rims_on_size', Rims.size)
Index('index_rims_on_description', Rims.description)


class Wheel:
    def __init__(self, hub_id: int = None, rim_id: int = None, pattern: int = 3, spokes: int = 32,
                 nipple_length: int = 0):
        self.hub_id = hub_id
        self.rim_id = rim_id
        self.pattern = pattern
        self.spokes = spokes
        self.nipple_length = nipple_length
        self.nipple_length_for_display = "12mm"


def nipple_size_for_display(nipple_length):
    if nipple_length == 0:
        return "12mm"
    elif nipple_length == 1:
        return  "14mm"
    elif nipple_length == 3:
        return "16mm"


def wl_effective(hub, rim):
    return hub['wl'] - rim['osb']


def wr_effective(hub, rim):
    return hub['wr'] + rim['osb']


def spoke_lengths(wheel, hub, rim):
    if not wheel['spokes'] or not hub['dl'] or not hub['dr'] or not rim['erd'] or not wheel['pattern']:
        return 0, 0

    result_l = sqrt(
        ((hub['dl'] / 2 * sin(2 * pi * wheel['pattern'] / (wheel['spokes'] / 2))) ** 2) +
        ((rim['erd'] / 2 - ((hub['dl'] / 2) * cos(2 * pi * wheel['pattern'] / (wheel['spokes'] / 2)))) ** 2) +
        (wl_effective(hub, rim) ** 2)
    ) - (hub['s'] / 2) - wheel['nipple_length']

    result_l = round(result_l, 1)

    result_r = sqrt(
        ((hub['dr'] / 2 * sin(2 * pi * wheel['pattern'] / (wheel['spokes'] / 2))) ** 2) +
        ((rim['erd'] / 2 - ((hub['dr'] / 2) * cos(2 * pi * wheel['pattern'] / (wheel['spokes'] / 2)))) ** 2) +
        (wr_effective(hub, rim) ** 2)
    ) - (hub['s'] / 2) - wheel['nipple_length']

    result_r = round(result_r, 1)

    return result_l, result_r


class Mru:
    def __init__(self, l: list):
        self.queue = l

    def add(self, item):
        self.queue = [item] + self.queue
        self.queue = sorted(set(self.queue), key=lambda x: self.queue.index(x))

        if len(self.queue) >= 10:
            _ = self.queue.pop()


patterns = [
    (0, "0-cross (Radial)"),
    (1, "1-cross"),
    (2, "2-cross"),
    (3, "3-cross"),
    (4, "4-cross"),
    (5, "5-cross"),
]

nipple_corrections = [
    (0, "12mm"),
    (1, "14mm"),
    (3, "16mm")
]

spoke_counts = [(16, 16), (20, 20), (24, 24), (28, 28), (32, 32), (36, 36), (40, 40), (48, 48)]

rim_sizes = [
    (622, '(622) 700C, 29"'),
    (559, '(559) 26 x 1.00- x 2.125'),
    (584, '(584) 650B / 26.5"'),
    (630, '(630) 27"'),
    (787, '(787) 36"'),
    (635, '(635) 28 x 1 1/2, 700 B'),
    (571, '(571) 650C, 26 x 1, 26 x 1 3/4'),
    (540, '(540) 24 x 1 3/8'),
    (520, '(520) 24 x 1, 24 x 1 1/8'),
    (507, '(507) 24 x 1.5-24 x 2.125'),
    (451, '(451) 20 x 1 1/8; x 1 1/4; x 1 3/8'),
    (406, '(406) 20 x 1.5- x 2.125'),
    (349, '(349) 16 x 1 3/8'),
    (305, '(305) 16 x 1.75- x 2.125'),
]

rim_sizes_for_display = {
    622: '700C, 29"',
    559: '26 x 1.00- x 2.125',
    584: '650B / 26.5"',
    630: '27"',
    787: '36"',
    635: '28 x 1 1/2, 700 B',
    571: '650C, 26 x 1, 26 x 1 3/4',
    597: '26 x 1 1/4, 26 x 1 3/8',
    540: '24 x 1 3/8',
    520: '24 x 1, 24 x 1 1/8',
    507: '24 x 1.5-24 x 2.125',
    451: '20 x 1 1/8; x 1 1/4; x 1 3/8',
    406: '20 x 1.5- x 2.125',
    349: '16 x 1 3/8',
    305: '16 x 1.75- x 2.125',
}

if __name__ == '__main__':

    import os
    import importlib
    from sqlalchemy import create_engine

    wb_config = os.environ.get('WB_CONFIG', 'DevelopmentConfig')
    config = getattr(importlib.import_module('config'), wb_config)

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
