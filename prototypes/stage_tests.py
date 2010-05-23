import stage
import unittest

class TestStage(unittest.TestCase):    
    def setUp(self):
        self.stage = stage.Stage()
        
    def __assertHasRoom(self, name, attr, looks='', exits=()):
        self.assertEqual(name, self.stage.room(name).name)
        self.assertEqual(looks, self.stage.room(name).looks_like())
        self.assertEqual(exits, self.stage.room(name).exits())
        self.assertTrue(hasattr(self.stage, attr))
        self.assertEqual(name, self.stage.__getattribute__(attr).name)
        self.assertEqual(looks, self.stage.__getattribute__(attr).looks_like())
        self.assertEqual(exits, self.stage.__getattribute__(attr).exits())
        
    def test_createRoom(self):
        self.stage.room('Cave 1')
        self.__assertHasRoom('Cave 1', 'cave_1')
        
    def test_describeRoom(self):
        description = 'This room has a chair.  The chair has a face.'
        self.stage.room('Living Room').looks_like(description)
        self.__assertHasRoom('Living Room', 'living_room', looks=description)
        
    def test_connectRoom(self):
        self.stage.room('Batcave').connects_to('Library')
        self.__assertHasRoom('Batcave', 'batcave', exits=('Library',))
        self.__assertHasRoom('Library', 'library')
        
    def test_connectMultipleRooms(self):
        self.stage.room('Forest').connects_to('House', 'Spooky Cave', 'River')
        self.stage.room('Spooky Cave').connects_to('Forest', 'Deep Cave')
        self.stage.room('House').connects_to('Forest')
        self.__assertHasRoom('Forest', 'forest', exits=('House', 'Spooky Cave', 'River'))
        self.__assertHasRoom('House', 'house', exits=('Forest',))
        self.__assertHasRoom('Spooky Cave', 'spooky_cave', exits=('Forest','Deep Cave'))
        self.__assertHasRoom('River', 'river')
        self.__assertHasRoom('Deep Cave', 'deep_cave')
        
    def test_connectAndDescribe(self):
        volcano_desc = '''This volcano is full of magma.  An evil landing pad on the side \
of the mountain marks a convenient place to land your evil hovercraft.  The valet is also evil.'''
        lair_desc = '''The evil lair has all the comforts of home.  Your favorite is an \
overstuffed chair with a mini fridge and launch codes for three countries' nuclear weapons.'''
        
        self.stage.room('Volcano').connects_to('Evil Lair').looks_like(volcano_desc)
        self.stage.room('Evil Lair').looks_like(lair_desc).connects_to('Volcano')
        self.__assertHasRoom('Volcano', 'volcano', looks=volcano_desc, exits=('Evil Lair',))
        self.__assertHasRoom('Evil Lair', 'evil_lair', looks=lair_desc, exits=('Volcano',))
        
    def test_changeDescription(self):
        self.stage.room('Hall of Mirrors').looks_like('You are in a maze of shiny mirrors, all alike')
        self.__assertHasRoom('Hall of Mirrors', 'hall_of_mirrors', 
                             looks='You are in a maze of shiny mirrors, all alike')
        self.stage.room('Hall of Mirrors').looks_like('You are shiny in an all-mirror maze, and they like you')
        self.__assertHasRoom('Hall of Mirrors', 'hall_of_mirrors',
                             looks='You are shiny in an all-mirror maze, and they like you')
                             
    def test_addConnections(self):
        self.stage.room('Flying Carpet').connects_to('Ground')
        self.__assertHasRoom('Flying Carpet', 'flying_carpet', exits=('Ground',))
        self.stage.room('Flying Carpet').connects_to('Sky')
        self.__assertHasRoom('Flying Carpet', 'flying_carpet', exits=('Ground', 'Sky'))
        
    def test_roomNameCollision(self):
        self.stage.room('Grue Home')
        self.assertRaises(ValueError, self.stage.room, 'gRUE hOME')
        
    def test_roomWithMethodName(self):
        self.assertRaises(TypeError, self.stage.room, 'room')
        
def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestStage)
    
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
        