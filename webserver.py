from BaseHTTPServer import *
import cgi
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Restaurant,MenuItem
from sqlalchemy import *

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/edit'):
                #First we extract the ID of the restaurant we need to edit
                #Can be obatined from the path
                restaurantID = self.path.split('/')[2]

                #Query the restaurant to retreive details
                restaurantFromID = session.query(Restaurant).filter(Restaurant.id == restaurantID).one()

                if restaurantID != [] :
                    # Valid response code
                    self.send_response(200)
                    # Used to signify that text in the form of HTML is being given to the client as a response
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    print "GET"

                    # Send output HTML
                    output = "<html><body>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/%s/edit'>" % restaurantID
                    output += "<h2>%s</h2>" % restaurantFromID.name
                    output += "<input name='name' type='text' value='%s'></br>" % restaurantFromID.name
                    output += "<input type='submit' placeholder='Rename'></form>"
                    output += "</body></html>"

                    self.wfile.write(output)
                    return

            elif self.path.endswith('/delete'):
                #First we extract the ID of the restaurant we need to delete
                #Can be obatined from the path
                restaurantID = self.path.split('/')[2]

                #Query the restaurant to retreive details
                restaurantFromID = session.query(Restaurant).filter(Restaurant.id == restaurantID).one()

                if restaurantID != [] :
                    # Valid response code
                    self.send_response(200)
                    # Used to signify that text in the form of HTML is being given to the client as a response
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    print "GET"

                    # Send output HTML
                    output = "<html><body>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/%s/delete'>" % restaurantID
                    output += "<h2>Would you like to delete %s from our Database?</h2>" % restaurantFromID.name
                    output += "<input type='submit' placeholder='Delete'></form>"
                    output += "</body></html>"

                    self.wfile.write(output)
                    return

            elif self.path.endswith('/restaurant'):
                #Valid response code
                self.send_response(200)
                #Used to signify that text in the form of HTML is being given to the client as a response
                self.send_header('Content-type','text/html')
                self.end_headers()
                print "GET"

                #Get result from DB
                restaurantResult = session.query(Restaurant).all()

                #Send output HTML
                output = "<html><body>"
                output += "<a href='/restaurant/new'>Add new Restaurant</a></br>"
                #Beginning of the FORM
                output += "<ul>"
                #Add results in the form of an unordered list
                for restaurant in restaurantResult:
                    output+= self.generateListItemFromString(restaurant)
                output += "</ul>"
                output+= "</body></html>"
                self.wfile.write(output)
                return

            elif self.path.endswith('/restaurant/new'):
                # Valid response code
                self.send_response(200)
                # Used to signify that text in the form of HTML is being given to the client as a response
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                print "GET"

                # Send output HTML
                output = "<html><body>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/new'>"
                output += "<h2>Enter the name of the new Restaurant</h2>"
                output += "<input name='name' type='text' value='Create a new Restaurant'></br>"
                output += "<input type='submit' placeholder='Create'></form>"
                output += "</body></html>"

                self.wfile.write(output)
                return

        except IOError:
            #Send error message if the file doesn't exist
            print self.send_error(404,"File not found %s" %self.path)

    def do_POST(self):
        try:
            if self.path.endswith('/restaurant/new'):

                print "POST"

                ctype, pdict = cgi.parse_header(self.headers.getheader("content-type"))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile,pdict)
                    restaurantName = fields.get('name')
                    print "Restaurant Name" , restaurantName

                #Add this to the database
                newRestaurant = Restaurant(name = restaurantName[0])
                session.add(newRestaurant)
                session.commit()

                # Send response as sucess
                self.send_response(301)
                self.send_header('Content-type','text/html')
                #This statement is creating a redirect to the main page
                self.send_header('Location','/restaurant')
                self.end_headers()

            elif self.path.endswith('/edit'):

                ctype, pdict = cgi.parse_header(self.headers.getheader("content-type"))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    updatedRestaurantName = fields.get('name')
                    print "New Restaurant Name", updatedRestaurantName[0]

                print "POST"

                restaurantID = self.path.split('/')[2]
                restaurantFromID = session.query(Restaurant).filter(Restaurant.id == restaurantID).one()

                #Update Value according to the response submitted
                restaurantFromID.name = updatedRestaurantName[0]
                session.add(restaurantFromID)
                session.commit()

                # Valid response code
                self.send_response(301)
                # Used to signify that text in the form of HTML is being given to the client as a response
                self.send_header('Content-type', 'text/html')
                self.send_header('Location','/restaurant')
                self.end_headers()

            elif self.path.endswith('/delete'):

                print "POST"

                restaurantID = self.path.split('/')[2]
                restaurantFromID = session.query(Restaurant).filter(Restaurant.id == restaurantID).one()

                #Remove the restaurant according to the response submitted

                session.delete(restaurantFromID)
                session.commit()

                # Valid response code
                self.send_response(301)
                # Used to signify that text in the form of HTML is being given to the client as a response
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurant')
                self.end_headers()

        except:
            pass

    def generateListItemFromString(self,x):
        return "<li><p>" +  x.name + "</p>" + "<a href='/restaurant/%s/edit'>Edit</a></br><a href='/restaurant/%s/delete'>Delete</a></li>" %(x.id,x.id)

def main():
    try:
        port = 8080
        #Create a server instance
        #Requires a tuple of ports and a server handler as arguements
        server = HTTPServer(('',port),webserverHandler)
        print "Server is running on port" , port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C was pressed , Stopping Web Server"
        server.socket.close()

if __name__ == '__main__':
    main()