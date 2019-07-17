# USAGE
# python barcode_scanner_video.py

# import the necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
import os

# def console clean
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
	help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# open the output CSV file for writing and initialize the set of
# barcodes found thus far
csv = open(args["output"], "w")
found = set()

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it to
	# have a maximum width of 400 pixels
	frame = vs.read()

	# -------------------------------------- #
	# ------------ uncommend --------------- #
	#
	# frame = imutils.resize(frame, width=800)
	#
	# ------------ uncommend --------------- #
	# -------------------------------------- #

	# find the barcodes in the frame and decode each of the barcodes
	barcodes = pyzbar.decode(frame)

	# loop over the detected barcodes
	for barcode in barcodes:
		# extract the bounding box location of the barcode and draw
		# the bounding box surrounding the barcode on the image
		(x, y, w, h) = barcode.rect
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

		# the barcode data is a bytes object so if we want to draw it
		# on our output image we need to convert it to a string first
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

		cls()
		print("url: "+barcodeData+"\n")
		print("SerialNo: "+serialNumber +"\n")
		print("Year: "+year +"\n")
		print("Factory: "+factory +"\n")
		print("Manufacturer: "+manufacturer +"\n")
		print("MaterialNo: "+materialNumber +"\n"+"\n")

		# draw the barcode data and barcode type on the image
		text = "{} ({})".format(barcodeData, barcodeType)
		cv2.putText(frame, text, (x, y - 10),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

		# if the barcode text is currently not in our CSV file, write
		# the timestamp + barcode to disk and update the set
		if barcodeData not in found:
			csv.write("{},{}\n".format(datetime.datetime.now(),
				barcodeData))
			csv.flush()
			found.add(barcodeData)

	# show the output frame
	cv2.imshow("Barcode Scanner", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# close the output CSV file do a bit of cleanup
print("[INFO] cleaning up...")
csv.close()
cv2.destroyAllWindows()
vs.stop()