
class StageState(object):
    def __init__(self):        
        self.rooms = { }
    
    def new_room(self, name):
        r = { 'name': name,
              'exits': [],
              'description' : '' }
        self.rooms[name] = r
        return r    

class Stage(object):    
    def __init__(self):
        self.__stage = StageState()    
        
    def __room_name(self, name):
        return name.lower().replace(' ', '_')
        
    def room(self, name):
        if name not in self.__stage.rooms:
            r = self.__stage.new_room(name)
        else:
            r = self.__stage.rooms[name]        

        room =  Room(self.__stage, r['name'])
        self.__setattr__(self.__room_name(name), room)
        return room
        
    #def __getattr__(self, name):
    #    for room_name in self.__stage.rooms:
    #        if name == room_name.lower().replace(' ', '_'):
    #            return Room(self.__stage, room_name)
        
class Room(object):    
    def __init__(self, stage, name):
        self.__stage = stage
        self.name = name
        
    def exits(self):
        return tuple(self.__stage.rooms[self.name]['exits'])
        
    def connects_to(self, *room_names):
        for name in room_names:
            if name not in self.__stage.rooms:
                self.__stage.new_room(name)
                            
            if name not in self.__stage.rooms[self.name]['exits']:
                self.__stage.rooms[self.name]['exits'].append(name)
                
        return self
                
    def looks_like(self, description=None):
        if description is None:
            return self.__stage.rooms[self.name]['description']
        else:
            self.__stage.rooms[self.name]['description'] = description
            return self
        