import rooms
import unittest

class TestRooms(unittest.TestCase):
    def setUp(self):
        self.caveZed = rooms.Room('Cave 0')
        self.caveOne = rooms.Room('Cave 1')
        self.caveTwo = rooms.Room('Cave 2')
        
    def test_roomNames(self):
        self.assertEqual('Cave 0', self.caveZed.name)
        
    def test_roomConnection(self):
        self.caveZed.connects_to(self.caveOne)
        self.assertTrue(self.caveOne in self.caveZed.exits)
        self.assertTrue(self.caveZed in self.caveOne.exits)
        
    def test_chainConnection(self):
        self.caveZed.connects_to(self.caveOne).connects_to(self.caveTwo)
        self.assertTrue(self.caveOne in self.caveZed.exits and
                        self.caveTwo in self.caveZed.exits and
                        self.caveZed in self.caveOne.exits and
                        self.caveZed in self.caveTwo.exits)        
        
def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestRooms) 
        
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())