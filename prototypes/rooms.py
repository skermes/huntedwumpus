class Room(object):    
    def __init__(self, name):        
        self.name = name
        self.exits = []
        
    def connects_to(self, other_room):
        self.exits.append(other_room)
        other_room.exits.append(self)
        return self