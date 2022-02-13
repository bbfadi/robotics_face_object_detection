 #showing a gray screen camera
'''
import numpy as np
import cv2
cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    frame = cv2.flip(frame,-1) #Flip Camera vertically
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame', frame)
    cv2.imshow('gray',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'): #q or CTRL C
        break
cap.release()
cv2.destroyAllWindows()
'''

# import the necessary packages
from __future__ import print_function
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import RPi.GPIO as GPIO
import os

from gpiozero import Buzzer
from time import sleep 
# initialize GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


#set buzzer at Pin 16
buzzer = 16
GPIO.setup(buzzer,GPIO.OUT)

def beep(mode):
    if (mode == "on"):
        GPIO.output(buzzer, GPIO.HIGH)
    else:
        GPIO.output(buzzer, GPIO.LOW)
 
def positionServo (servo, angle):
    os.system("python servocrtl.py " + servo + " " + str(angle))
    print("[INFO] Positioning servo at GPIO {0} to {1} degrees\n".format(servo, angle))


# position servos to present object at center of the frame
def mapServoPosition (x, y):
    print("[INFO] object center coordinates at X= {0} and Y = {1}".format(x,y))

    global panAngle
    global tiltAngle
    if (x < 210):
        panAngle+= 10
        if panAngle > 180:
            panAngle = 180
        positionServo ("pan", panAngle)

    if (x > 270):
        panAngle -= 10
        if panAngle < 0:
            panAngle = 0
        positionServo ("pan", panAngle)

    if (y < 160):
        tiltAngle -= 10
        print(' y <160 ==> Tilt Angle =  ' + str(tiltAngle))
        if tiltAngle < 60:
            tiltAngle = 60
        positionServo ("tilt", tiltAngle)
    
    if (y > 210):
        tiltAngle += 10
        print('y > 210 => Tilt Angle = ' + str(tiltAngle))
        if tiltAngle > 180:
            print("tilt extreme")
            tiltAngle = 180
        positionServo ("tilt", tiltAngle)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

# initialize the video stream and allow the camera sensor to warmup
print("[INFO] waiting for camera to warmup...")
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

# define the lower and upper boundaries of the object
# to be detected in the HSV color space
colorLower = (24, 100, 100) 
colorUpper = (44, 255, 255) 

#initialize servo positions
global panAngle
panAngle = 180
global tiltAngle
tiltAngle = 140
positionServo("pan", panAngle)
positionServo("tilt", tiltAngle)


# Start 
print("\n Starting..... ==> Press 'q' to quit Program \n")

# loop over the frames from the video stream
while True:
    # grab the next frame from the video stream, Invert 180o, resize the
    # frame, and convert it to the HSV color space
    frame = vs.read()
    frame = imutils.resize(frame, width=500)
    frame = imutils.rotate(frame, angle=180)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the obect color, then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the object
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    #cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    cnts = imutils.grab_contours(cnts) #from original
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        #print(cnts)
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 10:
            #print("radius = " + str(radius))
            if (radius > 90):
                beep("on")
            else:
                beep("off")


            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            #print("[INFO] object center coordinates at X= {0} and Y = {1}".format(x,y))
            
            #beep("on")
            mapServoPosition(int(x), int(y))
            #beep("off")

    # show the frame to our screen
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break



# do a bit of cleanup
print("\n Exiting Program and cleanup stuff \n")
GPIO.cleanup()
cv2.destroyAllWindows()
vs.stop()


