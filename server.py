import socket
import sys
import thread
import time
import pickle


# def serverFunctionalCode(connection, client_address):
#
#     global clientArray
#
#     #recieve signup or login mode choice
#     startupMode = connection.recv(4096)
#
#     if startupMode == 'L' or startupMode == 'l':
#         authResponse = 'NO'
#         i = 0
#         while True:
#             while authResponse != 'YES':
#                 #test authentication
#                 tmpUsr = connection.recv(4096)
#                 tmpPass = connection.recv(4096)
#                 for client in clientArray:
#                     if tmpUsr == client.username:
#                         if tmpPass == client.password:
#                             authResponse = 'YES'
#                             connectedUser = i
#                             break
#                         else:
#                             print >> sys.stderr, 'Wrong Password'
#                 i += 1
#                 connection.send(authResponse)
#
#         print >>sys.stderr, 'connection from', client_address
#
#     elif startupMode == 'S' or startupMode == 's':
#         print >> sys.stderr, 'Signup Mode Entered'
#         userAuth = 'NO'
#         while userAuth == 'NO':
#             userAuth = 'YES'
#             tmpUsr = connection.recv(4096)
#             for client in clientArray:
#                 if tmpUsr == client.username:
#                     userAuth = 'NO'
#                     break
#                 else:
#                     userAuth = 'YES'
#             connection.send(userAuth)
#
#
#         time.sleep(.3)
#         tmpPass = connection.recv(4096)
#
#         newClient = Client(tmpUsr, tmpPass)
#
#         clientArray.append(newClient)
#
#         connectedUser = len(clientArray) - 1
#
#
#
#         # Receive the data in small chunks and retransmit it
#         mode = 0
#         while True:
#             #get mode from client (option on menu picked)
#             print >> sys.stderr, 'Waiting on Mode Select'
#
#
#             mode = connection.recv(4096)
#
#
#             if (mode == '1'):
#                 #send a Snap
#                 connection.send(pickle.dumps(clientArray))
#
#                 tmpSnap = Snapchat()
#
#                 tmpSnap.sender = clientArray[connectedUser].username
#                 #recv user of whom to send snap
#                 reciever = int(connection.recv(4096))
#
#                 #recv message
#                 tmpSnap.messageData = connection.recv(4096)
#
#                 #recv timeout
#                 tmpSnap.timeoutLength = connection.recv(4096)
#
#                 clientArray[reciever].snapchats.append(tmpSnap)
#
#                 #print >> sys.stderr, clientArray[reciever].snapchats[0].messageData
#
#
#
#
#
#             elif(mode == '2'):
#                 # view My Snaps
#
#                 pickledClient = pickle.dumps(clientArray[connectedUser])
#
#                 connection.send(pickledClient)
#                 clientArray[connectedUser].snapchats = []
#             elif(mode == '3'):
#                 connection.close()
#                 return 0
#
#
#
#
#
#
#             else:
#                 print >> sys.stderr, 'Invalid choice must be 1, 2, or 3'

def serverFunctionalCode(connection, client_address):



    return


def serverInput():
    global clientArray



    while(True):
        #accepts input on server side for admin
        tmp=0;


    return 0


if __name__=='__main__':
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the port
    server_address = ('localhost', 7908)
    print >>sys.stderr, 'starting up on %s port %s' % server_address
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(5)
    #sock.setblocking(False)
    thread.start_new_thread(serverInput, ())
    while 1:
        print 'waiting for connection...'
        connection, client_address = sock.accept()
        print '...connected from:', client_address
        thread.start_new_thread(serverFunctionalCode, (connection, client_address))