#!/usr/bin/env python3

import urx
import logging
#import newdetect
import remotedetect
import operator
from pyzbar import pyzbar
import cv2
import numpy as np
import pyrealsense2 as rs
import time
import scipy.misc


#--------------------------------------------------------------------------------------------------------------

#Detection threshold
detect_thresh = 0.8

#Constants for movement
names = ["Base", "Shoulder", "Elbow", "Wrist1", "Wrist2", "Wrist3"]
#positions=[[-44, -90, 0, -90, 0, 0], [0, -90, 0, -90, 0, 0]]
home = [0,-90, 0, -90, 0, 0]
#positions_initialsweep = [[-78.37611915169416, -99.73683539439325, 66.41174122026771, -70.84466758017494, -88.19810205174267, 12.322350102625075], [-78.84397840773391, -144.82178262814003, 115.74842367961908, -92.82355612220445, -89.96818232657971, 15.446841716766357], [-27.865907037032038, -80.38545930431316, 53.78019733793416, -64.41214950191156, -118.24223251069594, 67.61799040873339], [-82.69042330912131, -52.319206857075514, 14.67937117169617, -50.530156360008306, -89.03366653752343, 8.140533403226524]]
positions_initialsweep = [[-78.37611915169416, -99.73683539439325, 66.41174122026771, -70.84466758017494, -88.19810205174267, 12.322350102625075], [-78.84397840773391, -144.82178262814003, 115.74842367961908, -92.82355612220445, -89.96818232657971, 15.446841716766357], [-27.865907037032038, -80.38545930431316, 53.78019733793416, -64.41214950191156, -118.24223251069594, 67.61799040873339]]
positions_3AE6  = [[-44, -40, 125, -70, 138, 7.2], [-41.25, -21.5, 98, -73.6, 141, 2.23], [-44, -40, 125, -70, 138, 7.2]]
positions_3AE55 = [[-38.48781008599079, -88.9972568314563, 55.712289870924245, -82.50534063661341, 146.3077842809592, 0.05289852125332898], [-38.48917681669901, -63.31931162761443, 124.88108227966697, -82.41180158694246, 146.29679576606506, 0.03366269746641065], [-38.48917681669901, 5.185020957023475, 78.98038815540872, -84.14369540579168, 146.29541536804976, 0.035723677990590307], [-60.371847516869444, 5.174715807483454, 75.17825266358199, -84.11753618003624, 120.68744677646905, -0.03571631771911521]]
positions_3AE53 = [[]]
#positions_3AE44 = [[]]

l = 0.05
v= 0.2
a= 0.2

#v = 0.40
#a = 0.40

#----------- ROB CONFIG
logging.basicConfig(level=logging.WARN)
tolerance = 15
rob = urx.Robot("192.168.117.117")
rob.set_tcp((0,0,0,0,0,0))
rob.set_payload(0.5, (0,0,0))
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
        print("moving to: " + str(pos))
        rob.movej(posdegtorad(pos), acc=a, vel=v)
def movetoallposback(positions, rob):  #do not use, robot controller does weird things
    for pos in reversed(positions):
        rob.movej(posdegtorad(pos), acc=0.10, vel=0.10)
def movetopos(position, rob):
    print("moving to: " + str(position))
    rob.movej(posdegtorad(position), acc=a, vel=v)

def vi(images):
    for image in images:
        cv2.namedWindow('Imagepreview', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('Imagepreview', image)
        cv2.waitKey(1)
        time.sleep(5)


def grabframe():
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
    pipeline.start(config)
    time.sleep(1)
    frames= pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    image = np.asanyarray(color_frame.get_data())
    pipeline.stop()
    return image

def grabframes(count):
    images = []
    for  i in range(count):
        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
        pipeline.start(config)
        time.sleep(1)
        frames= pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        image = np.asanyarray(color_frame.get_data())
        pipeline.stop()
        images.append(image)
    return images

def saveimages(images, prefix):
    names = []
    for index, image in enumerate(images):
        name = prefix + '_' +  str(index) + '.jpg'
#        scipy.misc.imsave(name, image)
        cv2.imwrite(name, image)
        names.append(name)
    return names


#---------------------------------------------------------------------------------------------------------------

def sweepandrec(rob): #does initial recording of 4 images to process by the graph
    images=[]
    for pos in positions_initialsweep:
        movetopos(pos, rob)
        images.append(grabframe())
    return images

def select_moveto_switch(switchtype, rob):
    print ("deciding next move on: " + switchtype)
    if switchtype == '3AE55':
        print("moving to 3AE55-pos")
        movetoallpos(positions_3AE55, rob)
    elif switchtype == '3AE53':
        print("moving to 3AE53-pos")
    #    movetoallpos(positions_3AE53, rob) #disabled because untested
    elif switchtype == '3AE6':
        print("moving to 3AE6-pos")
    #    movetoallpos(positions_3AE6, rob)  #disabled because untested
#    elif switchtype  == '3AE44':
#        print("moving to 3AE44-pos")
    #    movetoallpos(positions_3AE44, rob)  #disabled because untested
    return grabframe()

def barcodedecode(barcodes):
    barcodeType = barcode.type
    barcodeData = barcode.data.decode("utf-8")
    barcodeDataTmp = barcodeData.split("?")
    barcodeDataTmp = barcodeData[1]
    barcodeDataTmp = barcodeData.split("&")
    factory = barcodeDataTmp[2].split("=")
    factory = factory[1]

    # get serial number/typ
    serialNumber = barcodeDataTmp[0].split("=")
    serialNumber = serialNumber[1]
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
            
            detected_switch_dict  = remotedetect.detect(saveimages(sweepandrec(rob), 'sweep'))

            print(detected_switch_dict)
            firstobj = next(iter(detected_switch_dict.keys()))

            select_moveto_switch(firstobj, rob)


#finally>>> 
#            qrcodeimage= select_moveto_switch(remotedetect.detect(firstobj, rob)
#            print(barcodedecode(qrcodeimage))


    finally:
        rob.close()
