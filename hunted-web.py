import web

urls = (
    '/wumpus', 'Wumpus'
)
app = web.application(urls, globals())

class Wumpus:
    def GET(self):
        return "Hello, Wumpus." 
        
if __name__ == '__main__':
    app.run()