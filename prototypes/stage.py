
class _StageState(object):
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
        self.__stage = _StageState()    
        
    def __room_name(self, name):
        return name.lower().replace(' ', '_')
        
    def room(self, name):
        if name not in self.__stage.rooms:
            r = self.__stage.new_room(name)
        else:
            r = self.__stage.rooms[name]        

        room =  Room(self.__stage, r['name'])
        
        attr_name = self.__room_name(name)
        if not hasattr(self, attr_name):
            self.__setattr__(attr_name, room)
        elif not type(self.__getattribute__(attr_name)) == Room:
            raise TypeError('''I'm sorry, but you tried to make an object \
whose name resolves to '{0}', which is the name of a method that already \
exists on Stages. '''.format(attr_name))
        elif not self.__getattribute__(attr_name).name == name:
            raise ValueError('''I'm sorry, but you tried to make two \
objects that resolve to the same attribute name: '{0}'.  We don't support \
that right now.'''.format(attr_name))
        
        return room
        
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
        