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
#import base64
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




def getStock(message):
    DataObjectList = message.split()[-1]
    dataReceived = json.loads(DataObjectList)
    Newsymbol = dataReceived['symbol']


    response_buffer = BytesIO()
   # print(response_buffer)
    curl = pycurl.Curl()
    curl.setopt(curl.SSL_VERIFYPEER, False)
    curl.setopt(curl.URL, 'https://cloud.iexapis.com/stable/stock/' +Newsymbol+ '/chart/ytd?chartCloseOnly=true&token=pk_aff9e28203a3436cb258c9f4ec9f5dbb')

    #https://cloud.iexapis.com/stable/stock/symbol/chart/ytd?chartCloseOnly=true&token=yourAPIToken
    curl.setopt(curl.WRITEFUNCTION, response_buffer.write)

   # print("here is your response: ")

    curl.perform()
    curl.close()

    GraphdataReceived = json.loads(response_buffer.getvalue().decode('UTF-8'))
    #print("You receive data")

    body = json.dumps(GraphdataReceived)


    body2 = body.encode()
    header = "HTTP/1.1 200 OK\r\n\r\n".encode()
    return header, body2



def stock(resource):
    FileName = resource + ".html"

    header, body = getFile(FileName)
    return header, body

def findHeader(message,header):
    if message.find(header) > -1:
        value = message.split(' ')[1]
    else:
        value = None

    return value

# def checkUserDetails(authorizationHeader):
#      print(authorizationHeader)
#      username = "123"
#      password = "123"
#      encodedUserName = authorizationHeader.split()[-1]
#      if encodedUserName == base64.b64encode(username + ":" + password):
#          return  True

#
def login(message):
     json.loads(message)
     print(message)
     authorization_header = findHeader(message,'Authorization')



      #header = "HTTP/1.1 401 Authorization Required\r\nWWW-Authenticate: Basic realm='Private'".encode()
      #authorization_header = getHeader(message,'Authorization')
     print(authorization_header)
     if authorization_header == None:
          print("No authorization header")
          header = "HTTP/1.1 401 Authorization Required\r\nWWW-Authenticate: Basic realm='Private'".encode()
          print("No authorization header")
          return header,"".encode()



      # if authorization_header != None and checkUserDetails(authorization_header):
      #     print("go")
      # #       header = "HTTP/1.1 200 OK\r\n\r\n".encode()
      # #       return header,"".encode()
      # else:
      #      print("Not authorized")
      # #      header = "HTTP/1.1 401 Authorization Required\r\nWWW-Authenticate: Basic realm='Private'".encode()
      # #      print("No authorization header")
      # #      return header,"".encode()




      #header = "HTTP/1.1 401 Authorization Required\r\nWWW-Authenticate: Basic realm='Private'".encode()

#       splitMessage = message.split()
#       authorization_header = getHeader(message,'Authorization')
# # #
# # #       #if authorization_header != None and checkUserDetails(authorization_header):
#       if authorization_header == None:
#            header = "HTTP/1.1 401 Authorization Required\r\nWWW-Authenticate: Basic realm='Private'".encode()
#             header = "HTTP/1.1 401 Unauthorized WWW-Authenticate: Basic realm='Login.html', charset='UTF-8'\r\n".encode()
# #           header,body = "HTTP/1.1 401 Unauthorized www-Authenticate Basic realm='My Realm' charset='UTF-8' \r\n\r\n".encode()
# # #         #body = "WWW-Authenticate: Basic realm=<Login.html>,charset=<UTF-8>\r\n\r\n".encode()
# # #         body = "WWW-Authenticate: 'Basic' realm='Login.html'\r\n".encode()
#             body = ("<html><head></head><body><h1>Welcome to my homepage</h1></body></html>\r\n").encode()
      #return  "".encode(), "".encode()
#       else:
      #checkUserDetails(authorization_header)
     # else:
     #    header,body  = "HTTP/ 1.1 404 Not Found\r\n\r\n".encode()
     #
     #    return header,body
     #header, body = welcome(message)


#
# def login2(message):
#     print("Here is the message")
#     splitMessage = message.split()
#     print(splitMessage)
#     print("message end ")
#
#     authorization_header = getHeader(message,'Authorization')
#
#     if authorization_header != None and checkUserDetails(authorization_header):
#         header,body = "HTTP/1.1 200 OK\r\n\r\n".encode()
#         return header
#     else:
#         header = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
#         body = "<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode()
#        # header = www-Authenticate','Basic realm=["Login.html"].encode()
#        # header = 'WWW-Authenticate: Basic c,charset="UTF-8"\r\n\r\n'.encode()
#         #WWW-Authenticate: <type> realm=<realm>[, charset="UTF-8"]
#         #resp.headers['WWW-Authenticate'] = 'Basic'
#         return header,body


    #
    # foundInHeader = getHeader(message,'authorization')
    # b = message.find('authorization')
    #
    #
    # if foundInHeader == None :
    #     print("False")
    #     header  = 'www-Authenticate'
    #     err =  error("You are not authenticated!")
    #     return header, err
        #header  = 'www-Authenticate','Basic realm=["Login.html"]'

        #err.status = 401
    #print("true")

   #authHeader = message.headers.authorization

   # header = "HTTP/1.1 401 Unauthorized\r\n\r\n".encode()
   # return header



SymbolsList =[]
def getSymbols(resource):
    #SymbolsList =[]

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
       # print(object["symbol"])
        SymbolsList.append(object["symbol"])


    # Transform python object back into json
    body = json.dumps(SymbolsList)


    body2 = body.encode()
    header = "HTTP/1.1 200 OK\r\n\r\n".encode()
    return header, body2


def validateSymbol(symbol):
    if symbol in SymbolsList:
        return True
    else:
        return False


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

def getOldStockPrice(Getsymbol):

    with open('portfolio.json') as json_file:
        body = json_file.read()
        data = json.loads(body)


        for i in data:
            if(Getsymbol == i['symbol']):
               # print(i['price'])
                return(i['price'])


def getOldQuantity(Getsymbol):

    with open('portfolio.json') as json_file:
        body = json_file.read()
        data = json.loads(body)


        for i in data:
            if(Getsymbol == i['symbol']):
              #  print(i['quantity'])
                return(i['quantity'])




def getNewStockPrice(message):
     DataObjectList = message.split()[-1]
     dataReceived = json.loads(DataObjectList)
     symbol = dataReceived["symbol"]
     newSP = getStockPrice(symbol) # latest stock price
     body = json.dumps(newSP)
     body2 = body.encode()
     header = "HTTP/1.1 200 OK\r\n\r\n".encode()
     return header, body2



def portfolio(resource):

    FileName = resource + ".html"
    header, body = getFile(FileName)
    return header, body

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

     for i in data:
         if(Getsymbol in i['symbol']):
             checkSybolInJSONFIle = True
             i['price'] = averagePrice
             i['gain/loss'] = GainOrLoss
             i['quantity'] = NewQuantity


     if(checkSybolInJSONFIle == False):
         newData = {'symbol': Getsymbol, 'quantity': quantity, 'price': priceFloat, 'gain/loss': GainOrLoss}

         data.append(newData)


     with open('portfolio.json', 'w') as f:
        json.dump(data, f)




def SendData(message):

    DataObjectList = message.split()[-1]
    dataReceived = json.loads(DataObjectList)
    symbol = dataReceived["symbol"]
    quantity = dataReceived["quantity"]
    price = dataReceived["price"]
    validSymbol = validateSymbol(symbol)
   # if  validSymbol == False:
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
             responseHeader,responseBody = login(message)
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





