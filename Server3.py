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
import _thread
from socket import *
import pycurl
from io import BytesIO
import json
#from flask import Flask, request, Response

from flask import Flask, request, Response
import base64
from functools import wraps



serverSocket = socket(AF_INET, SOCK_STREAM)

serverPort = 8080
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(("", serverPort))

serverSocket.listen(5)




print('The server is running')
#loginVariable = False
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
   # header = 'www-Authenticate','Basic realm=["Login.html"]'

    header, body = welcome(message)
    return header, body



#Function retrieves stock data to present in graph
def getStock(message):
    DataObjectList = message.split()[-1]
    dataReceived = json.loads(DataObjectList)
    Newsymbol = dataReceived['symbol']


    response_buffer = BytesIO()
   # print(response_buffer)
    curl = pycurl.Curl()
    curl.setopt(curl.SSL_VERIFYPEER, False)
    curl.setopt(curl.URL, 'https://cloud.iexapis.com/stable/stock/' +Newsymbol+ '/chart/ytd?chartCloseOnly=true&token=pk_aff9e28203a3436cb258c9f4ec9f5dbb')


    curl.setopt(curl.WRITEFUNCTION, response_buffer.write)

   # print("here is your response: ")

    curl.perform()
    curl.close()

    GraphdataReceived = json.loads(response_buffer.getvalue().decode('UTF-8'))


    body = json.dumps(GraphdataReceived)


    body2 = body.encode()
    header = "HTTP/1.1 200 OK\r\n\r\n".encode()
    return header, body2


#Function calls  html page with stock graph to load
def stock(resource):
    FileName = resource + ".html"

    header, body = getFile(FileName)
    return header, body

#function checks if 'Autorization' is present in the header
def findHeader(message,header):
    for item in message:
        if header in item:
            return item
    else:
        return None


#Function confirms if user details are correct if not user cant login
def checkUserDetails(authorizationHeader):

    username = "18038659"
    password = "18038659"

    usrPass = (username +':'+password).encode("utf-8") #cchange login details from a sting to bytes
    encodedUserNameLogin = authorizationHeader.split(" ")[-1]
    decodedUserNameLogin = base64.b64decode(encodedUserNameLogin)


    if usrPass == decodedUserNameLogin: # check if provided login details bu user matches correct login details
        return True
    else:
        return False

#function used to check if user is logged in if not it promps the log in window
def login(message):
     splitMessage = message.split("\r\n")
     authorization_header = findHeader(splitMessage,'Authorization')




     if authorization_header == None:
          header = "HTTP/1.1 401 Authorization Required\r\nWWW-Authenticate: Basic realm='Private'".encode()
          return header,"".encode()



     if authorization_header != None and checkUserDetails(authorization_header):
          header = "HTTP/1.1 200 OK\r\n\r\n".encode()
          return None,None

     else:
          header = "HTTP/1.1 401 Authorization Required\r\nWWW-Authenticate: Basic realm='Private'".encode()
          return header,"".encode()

# Function retrieves stock symbols fom stock website and sort it for cs type then adds the symbols to a list
# The list of symbols are returned to the web browser through the body
SymbolsList =[]
def getSymbols(resource):


    response_buffer = BytesIO()

    curl = pycurl.Curl()
    curl.setopt(curl.SSL_VERIFYPEER, False)
    curl.setopt(curl.URL, 'https://cloud.iexapis.com/stable/ref-data/symbols?token=pk_aff9e28203a3436cb258c9f4ec9f5dbb')

    curl.setopt(curl.WRITEFUNCTION, response_buffer.write)

    print("here is your response: ")

    curl.perform()
    curl.close()

    dataReceived = json.loads(response_buffer.getvalue().decode('UTF-8'))

    # Filter python objects with list comprehensions
    output_dict = [x for x in dataReceived if x['type'] == 'cs']

    for object in output_dict:
        SymbolsList.append(object["symbol"])


    # Transform python object back into json
    body = json.dumps(SymbolsList)


    body2 = body.encode()
    header = "HTTP/1.1 200 OK\r\n\r\n".encode()
    return header, body2

#Function checks if symbol send through is in the list of symbols
def validateSymbol(symbol):
    if symbol in SymbolsList:
        return True
    else:
        return False

#Function retrieves the required symbols stock price fom stock web site
priceList =[]
def getStockPrice(symbol):

    response_buffer = BytesIO()
   # print(response_buffer)
    curl = pycurl.Curl()
    curl.setopt(curl.SSL_VERIFYPEER, False)
    curl.setopt(curl.URL, 'https://cloud.iexapis.com/stable/stock/' +symbol+ '/quote?token=pk_aff9e28203a3436cb258c9f4ec9f5dbb')

    curl.setopt(curl.WRITEFUNCTION, response_buffer.write)

   # print("here is your response: ")

    curl.perform()
    curl.close()

    dataReceived = json.loads(response_buffer.getvalue().decode('UTF-8'))
   # print(dataReceived)

    latestPrice = dataReceived['latestPrice']
    return(latestPrice)

#function retrieves stock price of requested stock symbol stored in JSON file
def getOldStockPrice(Getsymbol):

    with open('portfolio.json') as json_file:
        body = json_file.read()
        data = json.loads(body)


        for i in data:
            if(Getsymbol == i['symbol']):
               # print(i['price'])
                return(i['price'])

#function retrieves quantities of requested stock symbol stored in JSON file
def getOldQuantity(Getsymbol):

    with open('portfolio.json') as json_file:
        body = json_file.read()
        data = json.loads(body)


        for i in data:
            if(Getsymbol == i['symbol']):
              #  print(i['quantity'])
                return(i['quantity'])



#Function is used to retrieve the stock symbol to get the stock price from stoc server
def getNewStockPrice(message):
     DataObjectList = message.split()[-1]
     dataReceived = json.loads(DataObjectList)
     symbol = dataReceived["symbol"]
     newSP = getStockPrice(symbol) # latest stock price
     body = json.dumps(newSP)
     body2 = body.encode()
     header = "HTTP/1.1 200 OK\r\n\r\n".encode()
     return header, body2


#function used to load portfolio html file
def portfolio(resource):

    FileName = resource + ".html"
    header, body = getFile(FileName)
    return header, body

#function us used to set the values of portfolio table as well as check validitity of values send through to server.
def ResetTableWithLatestValues(Getsymbol,quantity,price,getLatestPrice, getOldPrice,OldQuantityValue, datareceivedThroughInput):

     if OldQuantityValue == None:
         OldQuantityValue = 0


     priceFloat = float(price)

     if priceFloat < 0:
         return False


     averagePrice = round((float(price) + float(getLatestPrice))/2,2)

     if priceFloat == 0:
         GainOrLoss = 0
     else:
         GainOrLoss = round(((getLatestPrice - priceFloat) / priceFloat)*100,2)

     NewQuantity = int(OldQuantityValue) + int(quantity)

     checkSybolInJSONFIle = False

     if NewQuantity < 0:
         return False

     a_file = open("portfolio.json", "r")
     data = json.load(a_file)
     a_file.close()

     for i in data:  # if symbol is in the json file update the values
         if(Getsymbol == i['symbol']):
             checkSybolInJSONFIle = True
             i['price'] = averagePrice
             i['gain/loss'] = GainOrLoss
             i['quantity'] = NewQuantity

     #if stock symbol is not in the JSON file then add the symbol
     if(checkSybolInJSONFIle == False):
         newData = {'symbol': Getsymbol, 'quantity': quantity, 'price': priceFloat, 'gain/loss': GainOrLoss}

         data.append(newData)

    # update the JSON file
     with open('portfolio.json', 'w') as f:
        json.dump(data, f)



#function recieves vslues used to update the JSON file and send through an errot if the values send through is not valid
def SendData(message):

    DataObjectList = message.split()[-1]
    dataReceived = json.loads(DataObjectList)
    symbol = dataReceived["symbol"]
    quantity = dataReceived["quantity"]
    price = dataReceived["price"]
    validSymbol = validateSymbol(symbol)
    getLatestPrice = getStockPrice(symbol)
    getOldPrice = getOldStockPrice(symbol)
    getOldQuantityValue = getOldQuantity(symbol)
    ResetTable = ResetTableWithLatestValues(symbol,quantity,price,getLatestPrice, getOldPrice,getOldQuantityValue,dataReceived)
    if ResetTable == False:
         header = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
         body = "<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode()
    else:
         header = "HTTP/1.1 200 OK\r\n\r\n".encode()
         body = welcome(message)
    return header,body


#We process client request here. The requested resource in the URL is mapped to a service function which generates the HTTP reponse
#that is eventually returned to the client.
loginVariable = False
def process(connectionSocket) :
    # Receives the request message from the client
    message = connectionSocket.recv(1024).decode()
    #loginVariable = False


    if len(message) > 1:


        # Extract the path of the requested object from the message
        # Because the extracted path of the HTTP request includes
        # a character '/', we read the path from the second character
        resource = message.split()[1][1:]

        #map requested resource (contained in the URL) to specific function which generates HTTP response


        responseHeader, responseBody = login(message)  # automatically check if user login is valid if not header send back 401 error

        if responseHeader == None:
            if resource == "":
                responseHeader,responseBody = portfolio("portfolio")
            elif resource == "stock":
                responseHeader,responseBody = stock(resource)
            elif resource == "portfolio":
                responseHeader,responseBody = portfolio(resource)
            elif resource == "getSymbols":
                responseHeader,responseBody = getSymbols(resource)
            elif resource == "SendData":
                responseHeader,responseBody = SendData(message)
            elif resource == "getNewStockPrice":
                responseHeader,responseBody = getNewStockPrice(message)
            elif resource == "getOldStockPrice":
                responseHeader,responseBody = getOldStockPrice(message)
            elif resource == "getStock":
                responseHeader,responseBody = getStock(message)
            elif resource == "login":
                responseHeader,responseBody = portfolio(resource)
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





