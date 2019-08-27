# Importing required libaries
import cv2
import imutils
import numpy as np
import pytesseract
from PIL import Image


#########################                    THE START                              ############################


#################################################################################################################
#                                  Image Morphological Transformation


img = cv2.imread('image.png',cv2.IMREAD_COLOR)     # reading images 
img = cv2.resize(img, (200,100) )                  # resizing image for better result  !!!  parameters should be adjusted  !!!
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)       # converting  to gray scale images
gray = cv2.bilateralFilter(gray, 11, 17, 17)       # Blurring image to reduce noise and any background environment
edged = cv2.Canny(gray, 30, 200)                   # Perform Edge detection

##################################################################################################################
#                              PART 1: DETECTION OF LICENSE PLATES OF VEHICLES IN IMAGES

#  Note : This part is an attempt to detect/extract license plates of vehicles from images automatically.
#         This does not use the annotations from JSON file for extraction.



# Find contours in the edged image, keep only the significant ones 
cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
box = None

for c in cnts:
 # Approximating the contour
 peri = cv2.arcLength(c, True)
 approx = cv2.approxPolyDP(c, 0.018 * peri, True)
 
 # If our approximated contour has four points, then we have determined the bounding box over license plate
 if len(approx) == 4:
  box = approx
  break

 

if box is None:
 detected = 0
 print("No box detected")
else:
 detected = 1

if detected == 1:
 cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)

# Masking the part other than the number plate to reduce noise and background details
mask = np.zeros(gray.shape,np.uint8)
mask_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
mask_image = cv2.bitwise_and(img,img,mask=mask)

# Extracting the plate
(x, y) = np.where(mask == 255)
(topx, topy) = (np.min(x), np.min(y))
(bottomx, bottomy) = (np.max(x), np.max(y))
plate = gray[topx:bottomx+1, topy:bottomy+1]

#################################################################################################################
#                               PART 2: OCR LICENSE PLATE USING TESSERACT (GOOGLE OCR ENGINE)

#Attempt 1: To recognise each character individually from obtained tesseract text for removing non-alphanumeric characters

# OCR Engine
config = '-l eng --oem 1 --psm 3'
text = pytesseract.image_to_string(gray, config=config)

validChars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

cleanText = []      # for removing non-alphanumeric characters
detectedplate = []  # for storing clean detected number 
for char in text:
        if char in validChars:
                cleanText.append(char)

plate = ''.join(cleanText)
detectedplate.append(plate)
print("Detected Number is:",detectedplate)

##################################################################################################################
#Attempt 2: To recognise entire text from tesseract ocr

#Read the number plate
text = pytesseract.image_to_string(plate, config='--psm 11')
print("Detected Number is:",text)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Reasons for two attempts: 
# Sometimes some license plates gets recognised by either of two methods. But in some cases, OCR engine itself fails 
##################################################################################################################

###############################                       THE END                    #################################
 