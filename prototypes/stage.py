
class Stage(object):    
    def __init__(self):        
        self.__rooms = { }
        
    def __new_room(self, name):
        r = { 'name': name,
              'exits': [],
              'description' : '' }
        self.__rooms[name] = r
        return r
        
    def room(self, name):
        if name not in self.__rooms:
            r = self.__new_room(name)
        else:
            r = self.__rooms[name]        
            
        return RoomStage(self, r)
        
class RoomStage(object):    
    def __init__(self, stage, room):
        self.__stage = stage
        self.__room = room
    
    def name(self):
        return self.__room['name']
        
    def exits(self):
        return self.__room['exits']
        
    def connects_to(self, *room_names):
        for name in room_names:
            
            # This will make sure that the stage
            # implicitly creates any rooms that
            # are referenced here.
            r = self.__stage.room(name)
                            
            if name not in self.__room['exits']:
                self.__room['exits'].append(name)
                
        return AlsoConnector(self)
                
    def looks_like(self, description=None):
        if description is None:
            return self.__room['description']
        else:
            self.__room['description'] = description
            return AlsoConnector(self)
    
class AlsoConnector(object):
    def __init__(self, payload):
        self.__payload = payload
        
    def also(self):
        return self.__payload
        