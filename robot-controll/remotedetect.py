#!/usr/bin/env python3
import os
import numpy as np
import sys
import time
import requests
import base64
from bs4 import BeautifulSoup
import operator

#url='http://b.f33.org/post'
url='http://b.f33.org/detectapi'

username='obapi'
password='mCZ7fe4kP1Y4fQ=='
request="curl -s --request POST  --url http://b.f33.org/detectapi  --header 'Authorization: Basic b2JhcGk6bUNaN2ZlNGtQMVk0ZlE9PQ=='  --header 'Postman-Token: 11e60c3d-203a-4105-9f1a-1b0dceb8f04b'  --header 'cache-control: no-cache'  --header 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW'  --form imagefile=@"


def detect(imagelist):
    detections = {}
    for image in imagelist:
        if os.path.isfile(image):
            fullreq = request + str(image)
#            print ("full request: " + fullreq)
            result = os.popen(fullreq).read()
            parsed_html = BeautifulSoup(result, "lxml")
            types = parsed_html.find('p',attrs={"name":"type"}).text
            scores = parsed_html.find('p',attrs={"name":"scores"}).text
            print("image: " + str(image) + " switch detected: " + types)
            print("with score: " + scores)
            if types in detections:
                detections.update({types : max(detections.get(types), scores)})
            else: 
                detections.update({types : scores})
            print("detection added to list: " + str(detections))
        else:
            print("Image not found or not a file, skipping: ", image)
    maxresult = max(detections.items(), key=operator.itemgetter(1))[0]
    print ("highest ranking detection: " + str(maxresult))
    return {maxresult  : detections.get(maxresult)}

#TESTING

# objects
#images = {os.path.join(os.getcwd(), 'sweep_0.jpg'), os.path.join(os.getcwd(), 'sweep_1.jpg'),os.path.join(os.getcwd(), 'sweep_2.jpg'), os.path.join(os.getcwd(), 'sweep_3.jpg')} 
#images = {os.path.join(os.getcwd(), 'test1.jpg')}
#print ("detection results:")
#print (detect(images, detection_threshold))
#print("full returned result: " + str(detect(images) ))



