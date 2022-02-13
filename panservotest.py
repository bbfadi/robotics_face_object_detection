import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

# pan servo 
GPIO.setup(11,GPIO.OUT)

#11 is Pin amd 50 is the 50HZ PULSE
panservo = GPIO.PWM(11,50)
panservo.start(0) #PULSE OFF = 0 HTZ
time.sleep(2)

#print("Setting the PAN Servo to 0 degrees")
panservo.ChangeDutyCycle(3)
time.sleep(0.3)
panservo.ChangeDutyCycle(0)
time.sleep(0.7)


#print("Setting the PAN Servo to 90 degrees")
panservo.ChangeDutyCycle(8)
time.sleep(0.3)
panservo.ChangeDutyCycle(0)
time.sleep(0.7)

#print("Setting the PAN Servo back to 180 degrees")
panservo.ChangeDutyCycle(18)
time.sleep(0.3)
panservo.ChangeDutyCycle(0)
time.sleep(0.7)

#print("Setting the PAN Servo to 90 degrees")
panservo.ChangeDutyCycle(9)
time.sleep(0.3)
panservo.ChangeDutyCycle(0)
time.sleep(0.7)

#print("Setting the PAN Servo back to 0 degrees")
panservo.ChangeDutyCycle(3)
time.sleep(0.3)
panservo.ChangeDutyCycle(0)
time.sleep(0.7)



#print("Setting the PAN Servo to 90 degrees")
#panservo.ChangeDutyCycle(7)
#time.sleep(2)

#Clean Things Up at the end
panservo.stop()
#servo2.stop()
GPIO.cleanup()
print("Goodbye")


#tilt servo 
#GPIO.setup(12,GPIO.OUT)



#servo2 = GPIO.PWM(12,50)
#time.sleep(2)
#servo2.start(0) #PULSE OFF = 0 HTZ
#time.sleep(2)
#servo2.ChangeDutyCycle(2)
#time.sleep(2)
'''
print("now starting 0")

servo1.start(0) #PULSE OFF = 0 HTZ
print("Waiting for 2 seconds")
time.sleep(2)

#Let us Move the Servo
print("rotating 180 degrees in 10 steps")

#Duty Cycle variabl2

duty=2

#Loop for duty values from 2 to 12 ==> 0 to 180 Degrees
while duty <= 12:
    servo1.ChangeDutyCycle(duty)
    time.sleep(1)
    duty = duty + 1
    
    time.sleep(2)


#Turn back to 90 Degrees
print("Turning Back to 90 Degrees")
servo1.ChangeDutyCycle(7)

#Turn Back to 0 degrees
print("Turning back to 0 degrees")
servo1.ChangeDutyCycle(2)
time.sleep(0.5)
servo1.ChangeDutyCycle(0)


'''