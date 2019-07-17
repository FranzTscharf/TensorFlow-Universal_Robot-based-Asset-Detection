#!/usr/bin/env python3
import os
import cv2
import numpy as np
import tensorflow as tf
import sys
import time

start_time = time.time()

from object_detection.utils import label_map_util

MODEL_NAME = 'inference_graph'

CWD_PATH = os.getcwd()
PATH_TO_CKPT = 'graph.pb/frozen_inference_graph.pb'
PATH_TO_LABELS = 'annotations/map.pbtxt'
NUM_CLASSES = 6
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)
    
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
num_detections = detection_graph.get_tensor_by_name('num_detections:0')


def detect(imagelist, min_score_thresh):
    objects =[]    

    for image in imagelist:
        if os.path.isfile(image):
            image = cv2.imread(image)
            image_expanded = np.expand_dims(image, axis=0)
            (boxes, scores, classes, num) = sess.run([detection_boxes, detection_scores, detection_classes, num_detections], feed_dict={image_tensor: image_expanded})

            print("{} seconds ".format(time.time() - start_time))
            for index, value in enumerate(classes[0]):
                object_dict = {}
                if scores[0, index] > min_score_thresh: #FIXME rebuild selecting the highest scoring detection
                    object_dict[(category_index.get(value)).get('name')] = scores[0, index]
                    objects.append(object_dict)
        else: 
            print("Image not found, skipping: ", image)
    return objects 


#FIXME TEST ONLY!
#images = {os.path.join(os.getcwd(), 'test1.jpg'), os.path.join(os.getcwd(), 'test2.jpg')}
images = {os.path.join(os.getcwd(), 'test1.jpg')}
foundobjects = detect(images, 0.6)
