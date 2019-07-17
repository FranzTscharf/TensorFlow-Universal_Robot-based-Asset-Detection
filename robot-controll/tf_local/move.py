#!/usr/bin/env python3

import urx
import logging
import newdetect
import operator
from pyzbar import pyzbar
import cv2


#--------------------------------------------------------------------------------------------------------------

#Constants for movement
names = ["Base", "Shoulder", "Elbow", "Wrist1", "Wrist2", "Wrist3"]
#positions=[[-44, -90, 0, -90, 0, 0], [0, -90, 0, -90, 0, 0]]
home = [0,-90, 0, -90, 0, 0]
positions_initialsweep = [[]]]
positions_switch1 = [[-44, -40, 125, -70, 138, 7.2], [-41.25, -21.5, 98, -73.6, 141, 2.23], [-44, -40, 125, -70, 138, 7.2]]
#TBD FIXME positions_switch2 = [[-44, -40, 125, -70, 138, 7.2], [-41.25, -21.5, 98, -73.6, 141, 2.23], [-44, -40, 125, -70, 138, 7.2]]
#TBD FIXME positions_switch3 = [[-44, -40, 125, -70, 138, 7.2], [-41.25, -21.5, 98, -73.6, 141, 2.23], [-44, -40, 125, -70, 138, 7.2]]
positions_switch2 = [[]]
positions_switch3 = [[]]
positions_switch4 = [[]]

l = 0.05
v = 0.40
a = 0.40

#----------- ROB CONFIG
logging.basicConfig(level=logging.WARN)
tolerance = 15
rob = urx.Robot("192.168.117.117")
rob.set_tcp((0,0,0,0,0,0))
rob.set_payload(0.5, (0,0,0))
camera = 0
imagewidth = 800
resize = 1

#--------------------------------------------------------------------------------------------------------------
#Functions for assistance with the whole rad/deg confusion
def degtorad (deg):
    return (3.14*deg)/180;
def radtodeg (rad):
    return (rad/3.14)*180;
def posradtodeg (radpos):
    for i,pos in enumerate(radpos):
        radpos[i]=radtodeg(pos)
    return radpos;
def posdegtorad (degpos):
    for i,pos in enumerate(degpos):
        degpos[i]=degtorad(pos)
    return degpos;

#--------------------------------------------------------------------------------------------------------------
#Function that is invoked bevore actual movement is taking place to check for possible collisions when homing
def checkhome (home, actual, tolerance):  #home = deg, actual = rad positions
	for hpos, apos, nm in zip(home, actual, names): 
		if ((hpos-tolerance)<radtodeg(apos) and radtodeg(apos)<(hpos+tolerance)): #actual check
                    print(nm, radtodeg(apos), " is near HOME: OK")                        #Validation IF within bounds
		else:
		    print(nm, radtodeg(apos),  " is NOT near HOME, ABORT")
		    return 1;                                                             #abort if out of range//away from home
#        print("done")
	return 0;


def movetoallpos(positions, rob):
    for pos in positions:
	rob.movej(posdegtorad(pos), acc=a, vel=v)


def checkforcode(frame):
    print("FIXME")

def grabvideoframe():
    image = cv2.VideoCapture(camera)
    if resize:
	image_width, image_height = image.size
	image_np = load_image_into_numpy_array(image)
	if (image_width < image_height):
	    tmpw = image_height
            tmph = image_width
            image_width = tmpw
            image_height = tmph
    imageScale = imagewidth/image_width
    newW,newH = image_width*imageScale, image_height*imageScale
    image = cv2.resize(image_np,(int(newW),int(newH)))

    return image

def sanitycheck (target, limit):
    for tpos, lpos in zip(target, limit):
#        if ()   #check if the target movement position potentially collides with WALL or MOUNT or SELF
        print("not implemented yet")

#---------------------------------------------------------------------------------------------------------------

def sweepandrec(rob, ): #does initial recording of 4 images to process by the graph
    
    return imagelist

def select_moveto_switch(objects, rob):
    #sort the dict of results:
    sorted_objects= sorted(objects[0].items(), key=operator.itemgetter(1)) #sort highest probability switch name to be the first in the list
    if sorted_objects[0][0] = '3AE51':
        movetoallpos(positions_switch1, rob)
    elif sorted_objects[0][0] = '3AE53':
        movetoallpos(positions_switch2, rob)
    elif sorted_objects[0][0] = '3AE6':
        movetoallpos(positions_switch3, rob)
    elif sorted_objects[0][0] = '3AE44':
        movetoallpos(positions_switch4, rob)
    return grabvideoframe()

def barcodedecode(barcodes):
    barcodeType = barcode.type
                barcodeData = barcode.data.decode("utf-8")
                barcodeDataTmp = barcodeData.split("?")
                barcodeDataTmp = barcodeData[1]
                barcodeDataTmp = barcodeData.split("&")
                # get factory
                factory = barcodeDataTmp[2].split("=")
                factory = factory[1]

                # get serial number/typ
                serialNumber = barcodeDataTmp[0].split("=")
                serialNumber = serialNumber[1]

                # get material number
                materialNumber = serialNumber.split("-")
                materialNumber = materialNumber[0]

                # get year of manufacturing
                year = barcodeDataTmp[1].split("=")
                year = year[1]

                # get manufacturer
                manufacturer = barcodeDataTmp[3].split("=")
                manufacturer = serialNumber[1]
        return  serialNumber;



#---------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        initj = rob.getj()
        print("Checking for being within +-", tolerance, "degrees of homeposition:", home)
        if not checkhome(home, initj, tolerance):
            print("Home check successfull, continuing...")
            print("Moving to precise home")
            rob.movej(posdegtorad(home), acc=a, vel=v)
            initj= rob.getj()
            print("Homed to ", posradtodeg(initj))
            print("moving to pos 0.1!...", positions[0])
            
            qrcodeimage= select_moveto_switch(newdetect(sweepandrec(rob)), rob)
            print(barcodedecode(qrcodeimage))
	    



    finally:
        rob.close()
