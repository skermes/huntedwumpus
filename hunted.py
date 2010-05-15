import random

def new_cavern(pits=2,bats=2):
    ''' Creates a new cave, based on the diagram
        for the original hunt the wumpus game:
        http://www.atariarchives.org/bcc1/showpage.php?page=247 '''
    assert pits + bats < 18
        
    caves = range(19)
    random.shuffle(caves)
        
    return { 'caves': [(1,2,8), (0,4,13), (0,3,5),
                       (2,4,6), (1,3,7), (2,9,10),
                       (3,10,11), (4,11,12), (0,9,19),
                       (5,8,14), (5,6,15), (6,7,16),
                       (7,13,17), (1,12,19), (9,15,18),
                       (10,16,14), (11,15,17), (12,16,18),
                       (14,17,19), (8,13,18)],
             'bats': caves[:bats],
             'pits': caves[bats:pits+bats],
             'wumpus': caves[pits+bats],
             'hunter': caves[pits+bats+1] }

def tell(cavern):
    ''' Prints some information about the player's 
        current position in the cavern. '''
    print 'You are in room', cavern['wumpus'], 'of the cavern.'    
    neighborhood = cavern['caves'][cavern['wumpus']]
    
    bats, pit = False, False
    for cave in neighborhood:
        if cave in cavern['bats'] and not bats:
            print 'You hear the rustling of leathery wings.'
            bats = True
        elif cave in cavern['pits'] and not pit:
            print 'You feel a draft from one of the nearby caves.'
            pit = True
        elif cave == cavern['hunter']:
            print 'You smell an unfamiliar creature.'
        
    print 'There are tunnels to caves', neighborhood[0], ',', neighborhood[1], ', and', neighborhood[2], '.'
             
def prompt():
    ''' Asks the player for the next action. '''
    return raw_input('Move or sleep? (m-s) ')

def move_to(destination, cavern):
    if destination not in cavern['caves'][cavern['wumpus']]:
        print 'What looked like a tunnel to cave', destination, 'was just an odd rock formation.  You can\'t get there from here.'
        return cavern
    
    cavern['wumpus'] = destination
    if destination in cavern['pits']:
        print 'You stumble into one of the cavern\'s bottomless pits.  Fortunately you\'re no stranger to these hazards, and pull yourself up with ease.'
    elif destination in cavern['bats']:
        print 'The air in this cave is filled with a swarm of giant bats.  They grab at you, but are unable to lift your bulk off the floor.'
    elif destination == cavern['hunter']:
        print 'You come face to face with a strange creature holding some pointed sticks.' # HUNTER ACTION
    
    return cavern
    
def new_hunter(cavern):
    caves = set(range(19))
    caves -= set(cavern['bats'])
    caves -= set(cavern['pits'])
    caves -= set([cavern['wumpus']])
    cavern['hunter'] = random.choice(list(caves))
    return cavern
    
def move_hunter(cavern):
    destination = random.choice(cavern['caves'][cavern['hunter']])
    
    if destination in cavern['pits']:
        print 'In the distance, you hear a cry as something tumbles into one of the cavern\'s bottomless pits.'
        cavern = new_hunter(cavern)
    elif destination in cavern['bats']:
        print 'An animal yelling somewhere in the caverns tells you that the superbats have captured something.'
        cavern = new_hunter(cavern)
    elif destination == cavern['wumpus']:
        print 'Suddenly, a strange creature holding some pointed sticks enters your cave!' # HUNTER ACTION
        
    return cavern
    
def do(action, cavern):
    if action.startswith('m'):
        destination = int(action[1:])
        cavern = move_to(destination, cavern)
    else:
        print 'You aren\'t sure what you just tried to do, but you are sure that you\'d rather not repeat the experiment.'
        
    return move_hunter(cavern)
             
def begin():
    ''' Starts a new game. '''
    cavern = new_cavern()    
    tell(cavern)    
    return cavern
             
if __name__ == '__main__':
    cavern = begin()
    while True:        
        action = prompt()
        print
        cavern = do(action, cavern)
        tell(cavern)
        print 