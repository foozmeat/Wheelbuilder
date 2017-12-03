import unittest

from wb.models import Hubs, Rims, Wheel, wl_effective, wr_effective, spoke_lengths


class WheelTests(unittest.TestCase):

    def setUp(self):
        h1 = Hubs()
        h1.description = "Shimano Dura-Ace"
        h1.s = 2.6
        h1.dl = 36.6
        h1.dr = 36.6
        h1.wl = 36.2
        h1.wr = 36.2
        h1.old = 100
        h1.forr = 'f'

        self.h1 = h1.as_dict()

        h2 = Hubs()
        h2.description = "Shimano Dura-Ace threaded"
        h2.s = 2.6
        h2.dl = 42.6
        h2.dr = 42.6
        h2.wl = 40.7
        h2.wr = 17.0
        h2.old = 130
        h2.forr = 'r'

        self.h2 = h2.as_dict()

        r1 = Rims()
        r1.description = "Alex Adventurer 2006"
        r1.erd = 603.1
        r1.osb = 0.0
        r1.size = "700C"
        r1.iso = 622
        self.r1 = r1.as_dict()

        r2 = Rims()
        r2.description = "Velocity Aerohead OC (Off Center)"
        r2.erd = 598
        r2.osb = 4.0
        r2.size = "700C"
        r2.iso = 622
        self.r2 = r2.as_dict()

        w1 = Wheel(spokes=36)
        self.front_wheel = w1.__dict__

        w2 = Wheel(spokes=36)
        self.rear_wheel = w2.__dict__

    def test_front_wl_effective(self):
        self.assertEqual(wl_effective(self.h1, self.r1), 36.2)

    def test_front_wr_effective(self):
        self.assertEqual(wr_effective(self.h1, self.r1), 36.2)

    def test_rear_wl_effective(self):
        self.assertEqual(wl_effective(self.h2, self.r2), 36.7)

    def test_rear_wr_effective(self):
        self.assertEqual(wr_effective(self.h2, self.r2), 21.0)

    def test_front_lengths(self):
        self.assertEqual(spoke_lengths(self.front_wheel, self.h1, self.r1), (293.8, 293.8))

    def test_rear_lengths(self):
        self.assertEqual(spoke_lengths(self.rear_wheel, self.h2, self.r2), (290.0, 288.4))
