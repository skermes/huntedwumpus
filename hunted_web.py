import web
import hunted

urls = (
    '/wumpus', 'Wumpus'
)
app = web.application(urls, globals())
render = web.template.frender('templates/hunted.html', globals={'str': str})

class Wumpus:
    def GET(self):
        cavern = hunted.begin(output=StringBuilder())        
        return render(cavern)
        
class StringBuilder:
    def __init__(self):
        self.__value = ''
       
    def write(self, data):
        self.__value += str(data)
        
    def __str__(self):
        return self.__value
       
if __name__ == '__main__':
    app.run()