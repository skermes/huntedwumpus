from json import loads as load_json
from json import dumps as dump_json

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
    def __init__(self, state=None):
        if state is None:
            self.__stage = _StageState()    
        else:
            self.__stage = state
        
    def __room_name(self, name):
        return name.lower().replace(' ', '_')
        
    def room(self, name):
        attr = self.__room_name(name)
        if hasattr(self, attr) and (type(getattr(self, attr)) != Room or getattr(self, attr).name != name):
            raise ValueError('''I'm sorrry, but the room you \
just tried to create ('{0}') would create an implicit attribute \
'{1}' on the stage.  The stage already has an attribute with that \
name, so I really can't let you do that.'''.format(name, attr))
        
        if name not in self.__stage.rooms:
            r = self.__stage.new_room(name)
        else:
            r = self.__stage.rooms[name]        

        return Room(self.__stage, r['name'])
        
    def json(self):
        return dump_json(self.__stage.rooms)
        
    def __getattribute__(self, name):
        stage = object.__getattribute__(self, '_Stage__stage')
        roomname = object.__getattribute__(self, '_Stage__room_name')
        for room in stage.rooms:
            if roomname(room) == name:
                return Room(stage, stage.rooms[room]['name'])
                
        return object.__getattribute__(self, name)
        
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
        
def json(input):
    data = load_json(input)
    state = _StageState()
    state.rooms = data
    return Stage(state)