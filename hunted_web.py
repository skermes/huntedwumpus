import web
import hunted

urls = (
    '/wumpus', 'Wumpus'
)
app = web.application(urls, globals())
render = web.template.render('templates')

class Wumpus:
    def GET(self):
        cavern = hunted.begin(output=StringBuilder())
        cavern['output'] = str(cavern['output'])
        return render.hunted(cavern)
        
    def POST(self):
        data = web.input()
        # TODO: Find a way to keep cavern state in the page 
        # that isn't vulnerable to hideous security holes.
        cavern = eval(data.cavern)
        cavern['output'] = StringBuilder(initial=cavern['output'])
        action = data.action
        if data.argument is not None and data.argument != '':
            argument = int(data.argument)
        else:
            argument = data.argument
        
        hunted.tell(cavern, '')
        cavern = hunted.do(action, argument, cavern)
        hunted.look(cavern)
        hunted.tell(cavern, '')
        
        cavern['output'] = str(cavern['output'])
        return render.hunted(cavern)
        
class StringBuilder:
    def __init__(self, initial=''):
        self.__value = initial
       
    def write(self, data):
        self.__value += str(data)
        
    def __str__(self):
        return self.__value
       
if __name__ == '__main__':
    app.run()