import socket
import sys
import thread
import time
import pickle
import os
# import RPi.GPIO as GPIO
from PIL import Image

imageMatrix = []
secondsToDisplayImage = 1.5


def loadImage(filename):
    image = Image.open(filename, 'r')
    imageRGBInfo = image.convert('RGB')
    width, height = imageRGBInfo.size
    print 'width = %d, height = %d' % (width, height)
    pixels = imageRGBInfo.load()
    # for x in range(width):
    #     for y in range(height):
    #         r,g,b = imageRGBInfo.getpixel((x,y))
    #         convertedMatrix[y][x] = makePixel(r,g,b)

    # To do: add resize here if image is not desired height

    # Calculate gamma correction table.  This includes
    # LPD8806-specific conversion (7-bit color w/high bit set).
    gamma = bytearray(256)
    for i in range(256):
        gamma[i] = 0x80 | int(pow(float(i) / 255.0, 2.5) * 127.0 + 0.5)

    # Create list of bytearrays, one for each column of image.
    # R, G, B byte per pixel, plus extra '0' byte at end for latch.
    print "Allocating..."
    column = [0 for x in range(width)]
    for x in range(width):
        column[x] = bytearray(height * 3 + 1)

    # Convert 8-bit RGB image into column-wise GRB bytearray list.
    print "Converting..."
    for x in range(width):
        for y in range(height):
            value = pixels[x, y]
            y3 = y * 3
            column[x][y3] = gamma[value[1]]
            column[x][y3 + 1] = gamma[value[0]]
            column[x][y3 + 2] = gamma[value[2]]

    return column, width, height


def serverFunctionalCode(connection, client_address):
    global imageMatrix, secondsToDisplayImage
    while True:
        # get mode from client (option on menu picked)
        print >> sys.stderr, 'Waiting on Mode Select from ', client_address
        mode = connection.recv(4096)
        # print 'Mode = %s' % mode

        if (mode == '1'):
            # load image
            clientType = connection.recv(4096)
            connection.sendto("Recieved Client type", client_address)
            print 'client Type recieved: %s' % clientType

            imageName = connection.recv(4096)
            connection.sendto("Recieved Image Name", client_address)
            print 'imageName: %s' % imageName

            sizeExpected = int(connection.recv(4096))
            connection.sendto("Recieved Size Expected", client_address)
            print 'sizeExpected: %d' % sizeExpected

            stringRecieved = ''
            fileWritten = False

            # recieve image and store in matrix
            if clientType == 'ios':
                print 'ios'
                imageFile = open(imageName, 'w')
                # get file for filename fro ios client also make sure file is BMP
                print 'file is correct'
                print 'Recieving Image'
                print 'beginning file size %d' % os.path.getsize(imageName)
                while not os.path.getsize(imageName) < sizeExpected:
                    data = connection.recv(4096)
                    imageFile.write(data)
                    print 'writing file total size %d' % os.path.getsize(imageName)

                imageFile.close()
                # convert it for use and store imageMatrix for Pickling
                imageMatrix, width, height = loadImage(imageName)
            elif clientType == 'python':
                print 'python'
                while sys.getsizeof(stringRecieved) < sizeExpected:
                    print 'begin size is: %d' % sys.getsizeof(stringRecieved)
                    stringRecieved += connection.recv(4096)
                    print 'end size is %d' % sys.getsizeof(stringRecieved)
                imageMatrix = pickle.loads(stringRecieved)

            pickleFileName = imageName + ".pickle"
            pickleFile = open(pickleFileName, "w")
            pickle.dump(imageMatrix, pickleFile)
            pickleFile.close()



            # sizeExpected = int(connection.recv(4096))
            # connection.sendto("Continue",client_address)
            # imageName = connection.recv(4096)
            # connection.sendto("Continue",client_address)
            # width = int(connection.recv(4096))
            # connection.sendto("Continue",client_address)
            # height = int(connection.recv(4096))
            # connection.sendto("Continue",client_address)
            # print 'Expeced %s bytes from %s' % (sizeExpected, client_address)
            # print 'int is %d' % int(sizeExpected)
            # stringRecieved = ''
            # while sys.getsizeof(stringRecieved) < sizeExpected:
            #     print 'begin size is: %d' % sys.getsizeof(stringRecieved)
            #     stringRecieved += connection.recv(4096)
            #     print 'end size is %d' % sys.getsizeof(stringRecieved)
            #
            # imageMatrix = pickle.loads(stringRecieved)
            # pickleFileName = imageName + ".pickle"
            # pickleFile = open(pickleFileName,"w")
            # pickle.dump(imageMatrix,pickleFile)
            # pickleFile.close()







        elif (mode == '2'):
            # display image
            imageName = connection.recv(4096)
            pickleFileName = imageName + ".pickle"
            pickleFile = open(pickleFileName, "r")
            diplayImage = pickle.load(pickleFile)

            # Then it's a trivial matter of writing each column to the SPI port.
            print "Displaying %s ... with width %d and height %d" % (imageName, width, height)
            for x in range(width):
                # spidev.write(column[x])
                sleepTime = float(secondsToDisplayImage) / float(width)
                time.sleep(sleepTime)
                # spidev.flush()
            time.sleep(0.5)
            connection.sendto("Done", client_address)
        elif (mode == '3'):
            # RECIEVE SECONDS TO DISPLAY IMAGE
            secondsToDisplayImage = int(connection.recv(4096))
            connection.sendto("Continue", client_address)
            print 'Display Seconds changed to %d seconds from ' % secondsToDisplayImage, client_address

        elif (mode == '4'):
            print 'Logout Recieved from ', client_address
            connection.close()
            return 0

        else:
            print >> sys.stderr, 'Invalid choice must be 1, 2, or 3'

    return


def serverInput():
    global clientArray

    while (True):
        # accepts input on server side for admin
        tmp = 0

    return 0


if __name__ == '__main__':
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the port
    server_address = ('0.0.0.0', 7907)
    print >> sys.stderr, 'starting up on %s port %s' % server_address
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)
    sock.setblocking(True)
    thread.start_new_thread(serverInput, ())
    while 1:
        print 'waiting for connection...'
        connection, client_address = sock.accept()
        print '...connected from:', client_address
        thread.start_new_thread(serverFunctionalCode, (connection, client_address))
