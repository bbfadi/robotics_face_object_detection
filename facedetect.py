'''
Face Tracking with OpenCV and Pan-Tilt controled servos 
    Based on a face detection tutorial on pythonprogramming.net
    Visit original post: https://pythonprogramming.net/haar-cascade-face-eye-detection-python-opencv-tutorial/
Developed by Marcelo Rovai - MJRoBot.org @ 7Feb2018 
'''

import numpy as np
import cv2
import os
import RPi.GPIO as GPIO

from gpiozero import Buzzer
from time import sleep 

from imutils.video import VideoStream
import argparse
import imutils
import time 


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

def positionServo(servo, angle):
    os.system("python servocrtl.py " + servo + " " + str(angle))
    print("[INFO] Positioning servo at GPIO {0} to {1} degrees\n".format(servo, angle))


#initialize servo positions
global panAngle
panAngle = 130
global tiltAngle
tiltAngle = 100
positionServo("pan", panAngle)
positionServo("tilt", tiltAngle)


# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

#cap = cv2.VideoCapture(0)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

# initialize the video stream and allow the camera sensor to warmup
print("[INFO] waiting for camera to warmup...")
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

startTime = time.time()
first_time_closed_detectecd = True

# Position servos to capture object at center of screen
def mapServoPosition(x, y):
    print("[INFO] object center coordinates at X= {0} and Y = {1}".format(x,y))
    global panAngle
    global tiltAngle
    if (x < 200):
        print(' Current pan Angle =  ' + str(panAngle))
        panAngle += 10
        if panAngle > 180:
            panAngle = 180
        print(' x <200 ==> pan Angle =  ' + str(panAngle))
        positionServo ("pan", panAngle)

    if (x > 270):
        print(' Current pan Angle =  ' + str(panAngle))
        panAngle -= 10
        if panAngle < 0:
            panAngle = 0
        print(' x  > 270 ==> Pan Angle =  ' + str(panAngle))
        positionServo ("pan", panAngle)

    if (y < 120):
        print(' Current Tilt Angle =  ' + str(tiltAngle))
        tiltAngle -= 10
        if tiltAngle < 60:
            print("tilt extreme")
            tiltAngle = 60
        print(' y <120 ==> Tilt Angle =  ' + str(tiltAngle))
        positionServo ("tilt", tiltAngle)
    
    if (y > 220):
        print(' Current Tilt Angle =  ' + str(tiltAngle))
        tiltAngle += 10
        if tiltAngle > 180:
            tiltAngle = 180
        print('y > 220 => Tilt Angle = ' + str(tiltAngle))
        positionServo ("tilt", tiltAngle)


while 1:
    img = vs.read()
    img = imutils.resize(img, width=500)
    img = imutils.rotate(img, angle=180)
    #hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #ret, img = cap.read()
    #img = cv2.flip(img, -1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if(len(faces)>0):
        for (x,y,w,h) in faces:
            mapServoPosition(int(x+w/2), int(y+h/2))
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            if (len(eyes)==0):
                if (first_time_closed_detectecd == True):
                    startTime = time.time()
                    first_time_closed_detectecd = False
                    print("StartTime = " + str(startTime))
                else:
                    print("Elapsed Time = " + str(time.time() - startTime))
                    if((time.time() - startTime) > 0.3):
                        beep("on")
                cv2.putText(img,
                "No Eye detected", (70,70),
                cv2.FONT_HERSHEY_PLAIN, 2,
                (0,0,255),2)
                #This will print on console and restart the algorithm
            
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color, (ex,ey), (ex+ew,ey+eh), (0,255,0),2)    
                first_time_closed_detectecd = True
                beep("off")
                #Examining the length of eyes object for eyes
                if(len(eyes)>=2):
                    #Check if program is running for detection
                    cv2.putText(img,
                    "Both Eyes open!", (70,70),
                    cv2.FONT_HERSHEY_PLAIN, 2,
                    (255,255,255),2)
                else:
                    if(len(eyes==1)):
                        #To ensure if the eyes are present before starting
                        cv2.putText(img,
                        "One Eye detected", (70,70),
                        cv2.FONT_HERSHEY_PLAIN, 2,
                        (255,255,255),2)
                
    else:
        cv2.putText(img,
        "No face detected",(100,100),
        cv2.FONT_HERSHEY_PLAIN, 3,
        (0,255,0),2)

    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break
    elif(k==ord('s') and first_read):
        #This will start the detection
        first_read = False
# do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff \n")
GPIO.cleanup()
vs.release()
cv2.destroyAllWindows()
