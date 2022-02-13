from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


def setServoAngle(servo, angle):
    if servo == "pan":
        assert angle >= 0 and angle <=180
    else:
        assert angle >= 60 and angle <=180
    
    servopin = 0
    if (servo == "pan"):
        servopin = 11
    else:
        servopin = 12
    #print("servo pin is = " + str(servopin))
    GPIO.setup(servopin, GPIO.OUT)
    pwm=GPIO.PWM(servopin,50)
    pwm.start(0)
    dutyCycle=(angle/18)+3
    #print("Calculated Duty Cycle based on given Angle " + str(angle) + "is = " + str(dutyCycle))
    pwm.ChangeDutyCycle(dutyCycle)
    sleep(0.3)
    pwm.stop()
if __name__ == '__main__':
    import sys
    servo = sys.argv[1]
    setServoAngle(servo, int(sys.argv[2]))
    #print("Cleanup and Goodbye")
    GPIO.cleanup()