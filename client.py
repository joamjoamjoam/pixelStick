import socket
import sys
import random
from PIL import Image
import time
import pickle

def makePixel(r, g, b):
    return (r<<24)|(g<<16)|(b<<8)|0xff

def rgbInfoForPixel(pixelAddress):
    """

    :rtype: 3 ints containg values from [0,255] represeting the color values of red green and blue for the specified pixels
    """
    r = pixelAddress>>24
    g = (pixelAddress>>16)&0xff
    b = (pixelAddress>>8)&0xff
    return (r,g,b)

width = 200
height = 200
imageMatrix = [[makePixel(124,32,243) for x in range(width)] for y in range(height)]


def loadImage(filename):
    image = Image.open(filename)
    image.show()
    return


if __name__=='__main__':
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 7908)
    print >>sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)
    r,g,b = rgbInfoForPixel(imageMatrix[3][3])

    print "number is %d, pixelInfo is (r, g, b) (%d, %d, %d)" % (imageMatrix[3][3],r,g,b)
    choice = '0'

    # client run code
    while choice == '0':

        print >> sys.stderr, '              --Menu--            '
        print >> sys.stderr, '1. Load Image'
        print >> sys.stderr, '2. View My Snaps'
        print >> sys.stderr, '3. Logout'
        choice = raw_input('>> ')
        absolutely_unused_variable = os.system("cls")
        absolutely_unused_variable = os.system("clear")

        if choice == '1':
            sock.sendto(choice, server_address)
            loadImageToMatrix()
            #send image to server for use
            choice = '0'
        elif choice == '2':
            sock.sendto(choice, server_address)

            choice = '0'

        elif choice == '3':
            sock.sendto(choice, server_address)
            print >> sys.stderr, 'Logged Out Succesfully.\nGoodbye.'

            sock.close()





        else:
            print >> sys.stderr, 'Invalid Choice'
            sock.sendto(choice, server_address)
            choice = '0'