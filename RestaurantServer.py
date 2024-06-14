from http.server import HTTPServer, BaseHTTPRequestHandler
from os import curdir, sep
from restaurantDatabase import RestaurantDatabase
import cgi

class RestaurantPortalHandler(BaseHTTPRequestHandler):
    
    def __init__(self, *args):
        self.database = RestaurantDatabase()
        BaseHTTPRequestHandler.__init__(self, *args)
    
    def do_POST(self):
        try:
            if self.path == '/addReservation':
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                customer_name = form.getvalue("customer_name")
                contact_info = form.getvalue("contact_info")
                reservation_time = form.getvalue("reservation_time")
                number_of_guests = form.getvalue("number_of_guests")
                special_requests = form.getvalue("special_requests")

                # Validate input
                if not customer_name or not contact_info or not reservation_time or not number_of_guests.isdigit():
                    self.send_error(400, "Invalid input data")
                    return

                number_of_guests = int(number_of_guests)
                
                
                # Call the Database Method to add a new reservation
                self.database.addReservation(customer_name, contact_info, reservation_time, number_of_guests, special_requests)
                print("Reservation added for customer:", customer_name)

                # Respond with a confirmation message
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                
                self.wfile.write(b"<html><head><title>Add Reservation</title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Reservation Added</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                 <a href='/addReservation'>Add Reservation</a>|\
                                 <a href='/viewReservations'>View Reservations</a></div>|\
                                 <a href='/addCustomer'>Add Customer</a></div>\
                                 ")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<h3>Reservation has been added</h3>")
                self.wfile.write(b"<div><a href='/addReservation'>Add Another Reservation</a></div>")
                self.wfile.write(b"</center></body></html>")
                
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

        return
    
    def do_GET(self):
        
        try:
            if self.path == '/':
                data=[]
                records = self.database.getAllReservations()
                print(records)
                data=records
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title>Restaurant Portal</title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Restaurant Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                 <a href='/addReservation'>Add Reservation</a>|\
                                  <a href='/viewReservations'>View Reservations</a></div>")
                self.wfile.write(b"<hr><h2>All Reservations</h2>")
                self.wfile.write(b"<table border=2> \
                                    <tr><th> Reservation ID </th>\
                                        <th> Customer Name </th>\
                                        <th> Contact Info </th>\
                                        <th> Reservation Time </th>\
                                        <th> Number of Guests </th>\
                                        <th> Special Requests </th></tr>")
                records = self.database.getAllReservations()
                for row in data:
                    self.wfile.write(b' <tr> <td>')
                    self.wfile.write(str(row[0]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[1]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[2]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[3]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[4]).encode())
                    self.wfile.write(b'</td></tr>')
                    self.wfile.write(str(row[5]).encode())
                    self.wfile.write(b'</td></tr>')
                
                self.wfile.write(b"</table></center>")
                self.wfile.write(b"</body></html>")
                return
            
            elif self.path =='/addReservation':
                # Respond with the form to add reservations
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                self.wfile.write(b"<html><head><title>Add Reservation</title></head>")

                self.wfile.write(b"<body>")

                self.wfile.write(b"<center><h2>Add Reservation</h2>")

                self.wfile.write(b"<form method='post' action='/addReservation'>")

                self.wfile.write(b"<label>Customer Name: </label>")

                self.wfile.write(b"<input type='text' name='customer_name' required><br>")

                self.wfile.write(b"<label>Contact Info: </label>")

                self.wfile.write(b"<input type='text' name='contact_info' required><br>")

                self.wfile.write(b"<label>Reservation Time: </label>")

                self.wfile.write(b"<input type='text' name='reservation_time' required><br>")

                self.wfile.write(b"<label>Number of Guests: </label>")

                self.wfile.write(b"<input type='text' name='number_of_guests' required><br>")

                self.wfile.write(b"<label>Special Requests: </label>")

                self.wfile.write(b"<input type='text' name='special_requests'><br>")

                self.wfile.write(b"<input type='submit' value='Submit'>")

                self.wfile.write(b"</form>")

                self.wfile.write(b"</center></body></html>")

                return
            


            if self.path =='/findReservations':
                return
            ## Add any other methods like addSpecialRequests etc
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

def run(server_class=HTTPServer, handler_class=RestaurantPortalHandler, port=8000):
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port {}'.format(port))
    httpd.serve_forever()

run()
