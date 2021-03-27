#Author: Sunil Lal

#This is a simple HTTP server which listens on port 8080, accepts connection request, and processes the client request 
#in sepearte threads. It implements basic service functions (methods) which generate HTTP response to service the HTTP requests. 
#Currently there are 3 service functions; default, welcome and getFile. The process function maps the requet URL pattern to the service function.
#When the requested resource in the URL is empty, the default function is called which currently invokes the welcome function.
#The welcome service function responds with a simple HTTP response: "Welcome to my homepage".
#The getFile service function fetches the requested html or img file and generates an HTTP response containing the file contents and appropriate headers.

#To extend this server's functionality, define your service function(s), and map it to suitable URL pattern in the process function.

#This web server runs on python v3
#Usage: execute this program, open your browser (preferably chrome) and type http://servername:8080
#e.g. if server.py and broswer are running on the same machine, then use http://localhost:8080



from socket import *
import _thread

serverSocket = socket(AF_INET, SOCK_STREAM)

serverPort = 8080
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(("", serverPort))

serverSocket.listen(5)
print('The server is running')	
# Server should be up and running and listening to the incoming connections

#Extract the given header value from the HTTP request message
def getHeader(message, header):

	if message.find(header) > -1:
		value = message.split(header)[1].split()[0]
	else:
		value = None

	return value

#service function to fetch the requested file, and send the contents back to the client in a HTTP response.
def getFile(filename):

	try:

		f = open(filename, "rb")
		# Store the entire content of the requested file in a temporary buffer
		body = f.read()

		# if the filename ends with (png||jpg) then set the Content-Type to be "image/(png||jpg)"
		if filename.endswith(('png', 'jpg')):
			contentType = "image/" + filename.split('.')[-1]
		# else set the Content-Type to be "text/html"
		else:
			contentType = "text/html"

		header = ("HTTP/1.1 200 OK\r\nContent-Type:" + contentType + "\r\n\r\n").encode()

	except IOError:

		# Send HTTP response message for resource not found
		header = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
		body = "<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode()

	return header, body

#service function to generate HTTP response with a simple welcome message
def welcome(message):


	header = "HTTP/1.1 200 OK\r\n\r\n".encode()
	body = ("<html><head></head><body><h1>Welcome to my homepage</h1></body></html>\r\n").encode()


	return header, body

#default service function
def default(message):

	header, body = welcome(message)

	return header, body


#We process client request here. The requested resource in the URL is mapped to a service function which generates the HTTP reponse 
#that is eventually returned to the client. 
def stock(resource):
	header, body = getFile(resource.html)
	return header, body



def process(connectionSocket) :
	# Receives the request message from the client
	message = connectionSocket.recv(1024).decode()


	if len(message) > 1:


		# Extract the path of the requested object from the message
		# Because the extracted path of the HTTP request includes
		# a character '/', we read the path from the second character
		resource = message.split()[1][1:]

		#map requested resource (contained in the URL) to specific function which generates HTTP response 
		if resource == "":
			responseHeader, responseBody = default(message)
		elif resource == "welcome":
			responseHeader,responseBody = welcome(message)
		elif resource == "stock":
			responseHeader,responseBody = stock(message)
		else:
			responseHeader,responseBody = getFile(resource)

	# Send the HTTP response header line to the connection socket
	connectionSocket.send(responseHeader)
	# Send the content of the HTTP body (e.g. requested file) to the connection socket
	connectionSocket.send(responseBody)
	# Close the client connection socket
	connectionSocket.close()


#Main web server loop. It simply accepts TCP connections, and get the request processed in seperate threads.
while True:
	
	# Set up a new connection from the client
	connectionSocket, addr = serverSocket.accept()
	#Clients timeout after 60 seconds of inactivity and must reconnect.
	connectionSocket.settimeout(60)
	# start new thread to handle incoming request
	_thread.start_new_thread(process,(connectionSocket,))





