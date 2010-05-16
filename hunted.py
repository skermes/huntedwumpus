import random, sys

__debugging = True

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
             'hunter': caves[pits+bats+1],
             'sleep': 0 }
             
def tell(cavern, *comments):
    ''' Works pretty much like a regular print call except that it won't write
        anything if the player is sleeping. '''
    if cavern['sleep'] < 1:
        sys.stdout.write(' '.join(str(c) for c in comments))
        sys.stdout.write('\n')

def look(cavern):
    ''' Prints some information about the player's 
        current position in the cavern. '''
    tell(cavern, 'You are in room', cavern['wumpus'], 'of the cavern.')
    neighborhood = cavern['caves'][cavern['wumpus']]
    
    bats, pit = False, False
    for cave in neighborhood:
        if cave in cavern['bats'] and not bats:
            tell(cavern, 'You hear the rustling of leathery wings.')
            bats = True
        elif cave in cavern['pits'] and not pit:
            tell(cavern, 'You feel a draft from one of the nearby caves.')
            pit = True
        elif cave == cavern['hunter']:
            tell(cavern, 'You smell an unfamiliar creature.')
        
    tell(cavern, 'There are tunnels to caves {0}, {1} and {2}.'.format(neighborhood[0], neighborhood[1], neighborhood[2]))
             
def prompt():
    ''' Asks the player for the next action. '''
    action = raw_input('Move or sleep? (m-s) ')
    if action == 'm':
        return action, int(raw_input('Where to? '))
    elif action == 's':
        return action, int(raw_input('How long? '))
    
    return action, None

def meet_hunter(cavern):
    ''' The wumpus meets the hunter!  What will happen? (hint: someone might get eated.) '''
    tell(cavern, 'You are frightened and confused by this hairless beast.  It yells and you lash out with one great paw.  The creature stops yelling, and doesn\'t get up from the floor.')
    return new_hunter(cavern)
    
def move_to(destination, cavern):
    ''' Moves the wumpus to the specified cave in the cavern, reporting the cave's state on the way. '''
    if destination not in cavern['caves'][cavern['wumpus']]:
        tell(cavern, 'What looked like a tunnel to cave', destination, 'was just an odd rock formation.  You can\'t get there from here.')
        return cavern
    
    cavern['wumpus'] = destination
    if destination in cavern['pits']:
        tell(cavern, 'You stumble into one of the cavern\'s bottomless pits.  Fortunately you\'re no stranger to these hazards, and pull yourself up with ease.')
    elif destination in cavern['bats']:
        tell(cavern, 'The air in this cave is filled with a swarm of giant bats.  They grab at you, but are unable to lift your bulk off the floor.')
    elif destination == cavern['hunter']:
        tell(cavern, 'You come face to face with a strange creature holding some pointed sticks.')
        cavern = meet_hunter(cavern)
    
    return cavern
    
def new_hunter(cavern):
    ''' Spawns a new hunter in the cavern, replacing the old one. '''
    caves = set(range(19))
    caves -= set(cavern['bats'])
    caves -= set(cavern['pits'])
    caves -= set([cavern['wumpus']])
    cavern['hunter'] = random.choice(list(caves))
    
    tell(cavern, 'You hear noise near the mouth of the cavern.')
    return cavern
    
def move_hunter(cavern):
    ''' Moves the hunter around the cavern, or has the hunter
        shoot an arrow if it's near the wumpus.  '''
    if cavern['wumpus'] in cavern['caves'][cavern['hunter']]:
        target = random.choice(cavern['caves'][cavern['hunter']])
        if target == cavern['wumpus']:
            cavern['sleep'] = 0
            tell(cavern, 'Out of nowhere, you feel something pierce your side.  As you lose consciousness, you see a strange creature run into the cave.  It looks happy.')
            sys.exit()
        elif random.random() < .4:
            tell(cavern, 'You hear a scream somewhere in cavern.')
            cavern = new_hunter(cavern)        
        else:
            tell(cavern, 'You hear an odd noise in the distance, like an animal throwing sticks around, though you can\'t imagine for what purpose.')
    else:
        destination = random.choice(cavern['caves'][cavern['hunter']])
        cavern['hunter'] = destination
        
        if destination in cavern['pits']:
            tell(cavern, 'In the distance, you hear a cry as something tumbles into one of the cavern\'s bottomless pits.')
            cavern = new_hunter(cavern)
        elif destination in cavern['bats']:
            tell(cavern, 'An animal yelling somewhere in the caverns tells you that the superbats have captured something.')
            cavern = new_hunter(cavern)
        elif destination == cavern['wumpus']:  
            cavern['sleep'] = 0
            tell(cavern, 'Suddenly, a strange creature holding some pointed sticks enters your cave!')
            cavern = meet_hunter(cavern)
        
    return cavern
    
def sleep(cavern, turns):
    ''' Makes the wumpus sleep for turns. The hunter keeps moving while
        the wumpus sleeps. '''
    cavern['sleep'] = turns
    while cavern['sleep'] > 0:
        cavern = move_hunter(cavern)
        cavern['sleep'] -= 1
    return cavern
    
def be_tired(cavern):
    ''' Informs the player that they are tired.  Players that are
        tired may fall asleep. '''        
    if cavern['sleep'] >= 0:
        pass
    elif -2 <= cavern['sleep'] <= -1:
        tell(cavern, 'You are feeling drowsy.')
    elif cavern['sleep'] == -3:
        tell(cavern, 'You are feeling sleepy.')
    elif cavern['sleep'] == -4:
        tell(cavern, 'You would really like a nap.')
    elif cavern['sleep'] == -5:
        tell(cavern, 'The outcropping in the corner looks like a nice bed.')
    elif cavern['sleep'] == -6:
        tell(cavern, 'You catch yourself nodding off as you walk through the cavern.')
    elif cavern['sleep'] == -7:
        tell(cavern, 'It\'s becoming very difficult to keep yourself awake.')
    elif cavern['sleep'] == -8:
        tell(cavern, 'You\'ve never forced yourself to stay awake this long before.')
    elif cavern['sleep'] == -9:
        tell(cavern, 'As you drag yourself through the cavern, you know you can\'t stay awake much longer.')
    elif cavern['sleep'] == -10:
        tell(cavern, 'You hear voices coming from other caves, but in your exhaustion, you can\'t tell if they\'re real or not.')
        
    fell_asleep = random.random() < (-cavern['sleep'] * .1)
    cavern['sleep'] -= 1
    
    return cavern, fell_asleep
    
def do(action, argument, cavern):        
    ''' Does an action in the cavern.  Currently, actions are moving, sleeping, debugging and exiting. '''
    if action == 'm':
        cavern, fell_asleep = be_tired(cavern)
        if fell_asleep:
            tell(cavern, 'Unable to remain awake, you collapse where you are and fall asleep.')
            sleep(cavern, random.randint(-2,2) + cavern['sleep'])
        else:            
            cavern = move_to(argument, cavern)
        return move_hunter(cavern)
    elif action == 's':
        cavern = sleep(cavern, argument)
        return cavern
    elif action == 'exit':
        sys.exit()
    elif action == 'debug' and __debugging:
        tell(cavern, cavern)      
        return cavern
    else:
        tell(cavern, 'You aren\'t sure what you just tried to do, but you are sure that you\'d rather not repeat the experiment.')
        return cavern
             
def begin():
    ''' Starts a new game. '''
    cavern = new_cavern()    
    look(cavern)    
    return cavern
             
if __name__ == '__main__':
    cavern = begin()
    while True:        
        action, arg = prompt()
        tell(cavern, '')
        cavern = do(action, arg, cavern)
        look(cavern)
        tell(cavern, '')