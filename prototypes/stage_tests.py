import stage
import unittest

class TestStage(unittest.TestCase):    
    def setUp(self):
        self.stage = stage.Stage()
        
    def test_createRoom(self):
        self.stage.room('Cave 1').connects_to('Cave 2', 'Cave 3').also().looks_like('This cave has shiny rocks in it.')
        self.assertEqual('Cave 1', self.stage.room('Cave 1').name())
        self.assertTrue(self.stage.room('Cave 2').name() in self.stage.room('Cave 1').exits() and
                        self.stage.room('Cave 3').name() in self.stage.room('Cave 1').exits())
        self.assertEqual('This cave has shiny rocks in it.', self.stage.room('Cave 1').looks_like())
        
def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestStage)
    
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
        