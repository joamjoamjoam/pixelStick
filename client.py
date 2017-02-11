import socket
import sys
import random
from PIL import Image
import time
import pickle
import os, sys

loadedImageNames = []


def makePixel(r, g, b):
    return (r << 24) | (g << 16) | (b << 8) | 0xff


def rgbInfoForPixel(pixelAddress):
    """

    :rtype: 3 ints containg values from [0,255] represeting the color values of red green and blue for the specified pixels
    """
    r = pixelAddress >> 24
    g = (pixelAddress >> 16) & 0xff
    b = (pixelAddress >> 8) & 0xff
    return (r, g, b)


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


if __name__ == '__main__':
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 7908)
    print >> sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)
    choice = '0'

    # load imageNames Array from server

    # client run code
    while choice == '0':

        print >> sys.stderr, '              --Menu--            '
        print >> sys.stderr, '1. Load Image'
        print >> sys.stderr, '2. Send Image'
        print >> sys.stderr, '3. Change Image Display Time'
        print >> sys.stderr, '4. Exit'
        choice = raw_input('>> ')
        absolutely_unused_variable = os.system("cls")
        absolutely_unused_variable = os.system("clear")

        if choice == '1':
            imageName = raw_input('Image File Name -> ')
            # add in check to see if image exists here
            imageMatrix, width, height = loadImage(imageName)
            loadedImageNames.append(imageName)
            if height <= 200:
                sock.sendto(choice, server_address)

                print imageMatrix[0][width - 1], width, height
                size = sys.getsizeof(pickle.dumps(imageMatrix))
                print('sending %d bytes' % size)

                sock.sendto("python", server_address)
                sock.recv(4096)
                sock.sendto(imageName, server_address)
                sock.recv(4096)
                sock.sendto(str(size), server_address)
                sock.recv(4096)
                sock.sendto('Sending File Info',server_address)
                sock.recv(4096)

                sock.sendto(pickle.dumps(imageMatrix), server_address)
            else:
                print 'image too tall. Must be less than 200 vertical pixels'
            # send image to server for use
            choice = '0'
        elif choice == '2':
            sock.sendto(choice, server_address)
            choice = '0'
            while choice == '0':
                # list loaded images
                for i in range(len(loadedImageNames)):
                    print '%d. %s' % (i + 1, loadedImageNames[i])
                choice = int(raw_input('Choose Image Number -> '))
                # input validation
                if choice > 0 and choice <= len(loadedImageNames):
                    # legit choice send filename
                    sock.sendto(loadedImageNames[choice - 1], server_address)
                    # wait for display of image to end
                    confirmation = sock.recv(4096)
                else:
                    print 'Please select a number from the list'
                    choice = '0'
            choice = '0'

        elif choice == '3':
            sock.sendto(choice, server_address)
            # change number of seconds to display image
            sent = False
            while sent == False:
                seconds = int(raw_input('Enter # of seconds to display image -> '))
                if seconds > 0 and seconds <= 10:
                    sock.sendto(str(seconds), server_address)
                    sock.recv(4096)
                    print '%d seconds set for Display Time' % seconds
                    sent = True
                else:
                    print '%d is not a valid number to set please try again' % seconds
            choice = '0'

        elif choice == '4':
            sock.sendto(choice, server_address)
            print >> sys.stderr, 'Logged Out Succesfully.\nGoodbye.'

            sock.close()





        else:
            print >> sys.stderr, 'Invalid Choice'
            sock.sendto(choice, server_address)
            choice = '0'
