import unittest

from wb.models import Hubs, Rims, Wheel


class WheelToots(unittest.TestCase):

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

        self.h1 = h1

        h2 = Hubs()
        h2.description = "Shimano Dura-Ace threaded"
        h2.s = 2.6
        h2.dl = 42.6
        h2.dr = 42.6
        h2.wl = 40.7
        h2.wr = 17.0
        h2.old = 130
        h2.forr = 'r'

        self.h2 = h2

        r1 = Rims()
        r1.description = "Alex Adventurer 2006"
        r1.erd = 603.1
        r1.osb = 0.0
        r1.size = "700C"
        r1.iso = 622
        self.r1 = r1

        r2 = Rims()
        r2.description = "Velocity Aerohead OC (Off Center)"
        r2.erd = 598
        r2.osb = 4.0
        r2.size = "700C"
        r2.iso = 622
        self.r2 = r2

        self.front_wheel = Wheel(h1, r1)
        self.front_wheel.spokes = 36

        self.rear_wheel = Wheel(h2, r2)
        self.rear_wheel.spokes = 36

    def test_front_wl_effective(self):
        self.assertEqual(self.front_wheel.wl_effective, 36.2)

    def test_front_wr_effective(self):
        self.assertEqual(self.front_wheel.wr_effective, 36.2)

    def test_rear_wl_effective(self):
        self.assertEqual(self.rear_wheel.wl_effective, 36.7)

    def test_rear_wr_effective(self):
        self.assertEqual(self.rear_wheel.wr_effective, 21.0)

    def test_front_l_length(self):
        self.assertEqual(self.front_wheel.l_length, 293.8)

    def test_front_r_length(self):
        self.assertEqual(self.front_wheel.r_length, 293.8)

    def test_rear_l_length(self):
        self.assertEqual(self.rear_wheel.l_length, 290.0)

    def test_read_r_length(self):
        self.assertEqual(self.rear_wheel.r_length, 288.4)
