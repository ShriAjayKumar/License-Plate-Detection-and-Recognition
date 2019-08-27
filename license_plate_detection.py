# Importing Required libaries
import json
import wget
import cv2 
import os
from math import floor as fl

# Source path for images 
filename = "C:\\Users\\Aj\\Desktop\\HumanAI\\vehicle-number-plate-detection Datasets\\Indian_Number_plates.json"
path = "C:\\Users\\Aj\\Desktop\\HumanAI\\vehicle-number-plate-detection Datasets\\data\\"
destination = "C:\\Users\\Aj\\Desktop\\HumanAI\\vehicle-number-plate-detection Datasets\\plates\\"

# change the working directory to save the extracted license plates 
os.chdir(destination)

# For reading each line as input and read JSON data
def json_readr(f):
    for line in open(f, mode="r"):
        yield json.loads(line)

# For reading JSON data file
with open(filename,'r') as obj:
    dataset = list(json_readr(filename)) 


count = 1
# for Loading URL from dictionary and storing images and  annotations of respective images
for it in range(len(dataset)):
    width = dataset[it]['annotation'][0]['imageWidth']
    height = dataset[it]['annotation'][0]['imageHeight']
    top_left_x = dataset[it]['annotation'][0]['points'][0]['x']
    top_left_y = dataset[it]['annotation'][0]['points'][0]['y']
    bottom_right_x = dataset[it]['annotation'][0]['points'][1]['x']
    bottom_right_y = dataset[it]['annotation'][0]['points'][1]['y']

    # reading vehicle images for cropping out license plates
    img =  cv2.imread("C:\\Users\\Aj\\Desktop\\HumanAI\\vehicle-number-plate-detection Datasets\\data\\image%d.png"%count,1)

    # using annotations( x and y points ) in json file for detection of license plates
    dx1 = fl(top_left_x*width)
    dx2 = fl(bottom_right_x*width)
    dy1 = fl(top_left_y*height)
    dy2 = fl(bottom_right_y*height)
    img = img[dy1:dy2,dx1:dx2]
    
    # storing the extracted license plates 
    cv2.imwrite('image%d.jpg'%count,img)
    count += 1
 