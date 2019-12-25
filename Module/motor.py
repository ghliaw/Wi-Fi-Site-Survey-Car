import RPi.GPIO as GPIO
from datetime import datetime
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False) 

# Pin 18 19 ; IN 1 2 ; pwm0=> 右後輪
# Pin 21 22 ; IN 3 4 ; pwm1=> 右前輪
# Pin 23 24 ; IN 5 6 ; pwm2=> 左後輪
# Pin 11 13 ; IN 7 8 ; pwm3=> 左前輪

class Direction():
    def __init__(self, dc = 35.0):    
        # motor
        GPIO.setup(18,GPIO.OUT)
        GPIO.setup(19,GPIO.OUT)
        GPIO.setup(21,GPIO.OUT)
        GPIO.setup(22,GPIO.OUT)
        GPIO.setup(23,GPIO.OUT)  
        GPIO.setup(24,GPIO.OUT)  
        GPIO.setup(38,GPIO.OUT)  
        GPIO.setup(40,GPIO.OUT)

        GPIO.output(18,GPIO.LOW)
        GPIO.output(19,GPIO.LOW)
        GPIO.output(21,GPIO.LOW)
        GPIO.output(22,GPIO.LOW)
        GPIO.output(23,GPIO.LOW)  
        GPIO.output(24,GPIO.LOW)
        GPIO.output(38,GPIO.LOW)  
        GPIO.output(40,GPIO.LOW)

        # pwm
        GPIO.setup(12,GPIO.OUT)
        GPIO.setup(32,GPIO.OUT)
        GPIO.setup(33,GPIO.OUT)
        GPIO.setup(35,GPIO.OUT)
        
        self.pwm0 = GPIO.PWM(12, 50.0)
        self.pwm1 = GPIO.PWM(32, 50.0)
        self.pwm2 = GPIO.PWM(33, 50.0)
        self.pwm3 = GPIO.PWM(35, 50.0)
        
        self.right_dc = dc
        self.left_dc = dc
        
        self.pwm0.start(self.right_dc)
        self.pwm1.start(self.right_dc)
        self.pwm2.start(self.left_dc)
        self.pwm3.start(self.left_dc)

    # car directions
    def Dir(self, dir):
        if dir == 'F':
            GPIO.output(19,GPIO.HIGH)
            GPIO.output(18,GPIO.LOW)
            GPIO.output(22,GPIO.HIGH)
            GPIO.output(21,GPIO.LOW)
            GPIO.output(23,GPIO.HIGH)
            GPIO.output(24,GPIO.LOW)     
            GPIO.output(40,GPIO.HIGH)
            GPIO.output(38,GPIO.LOW)
        if dir == 'R':
            GPIO.output(19,GPIO.LOW)
            GPIO.output(18,GPIO.HIGH)
            GPIO.output(22,GPIO.LOW)
            GPIO.output(21,GPIO.HIGH)
            GPIO.output(23,GPIO.HIGH)  
            GPIO.output(24,GPIO.LOW)  
            GPIO.output(40,GPIO.HIGH)  
            GPIO.output(38,GPIO.LOW) 
        if dir == 'L':
            GPIO.output(19,GPIO.HIGH)
            GPIO.output(18,GPIO.LOW)
            GPIO.output(22,GPIO.HIGH)
            GPIO.output(21,GPIO.LOW)
            GPIO.output(23,GPIO.LOW)  
            GPIO.output(24,GPIO.HIGH)  
            GPIO.output(40,GPIO.LOW)  
            GPIO.output(38,GPIO.HIGH) 
        if dir == 'B':
            GPIO.output(19,GPIO.LOW)
            GPIO.output(18,GPIO.HIGH)   
            GPIO.output(22,GPIO.LOW)
            GPIO.output(21,GPIO.HIGH)
            GPIO.output(23,GPIO.LOW)
            GPIO.output(24,GPIO.HIGH)
            GPIO.output(40,GPIO.LOW)
            GPIO.output(38,GPIO.HIGH)
        if dir == 'S':
            GPIO.output(19,GPIO.LOW)
            GPIO.output(18,GPIO.LOW)
            GPIO.output(22,GPIO.LOW)
            GPIO.output(21,GPIO.LOW)
            GPIO.output(23,GPIO.LOW)  
            GPIO.output(24,GPIO.LOW)  
            GPIO.output(40,GPIO.LOW)  
            GPIO.output(38,GPIO.LOW)
    
    # adjust car bias
    def Adjust(self, yaw):
        if (yaw < -0.5):
            self.left_dc = self.left_dc + 5.0
            self.right_dc = self.right_dc - 5.0
        elif (yaw > 0.5):
            self.left_dc = self.left_dc - 5.0
            self.right_dc = self.right_dc + 5.0
        
        if (self.right_dc > 100.0):
            self.right_dc = 100.0
        if (self.right_dc < 0.0):
            self.right_dc = 0.0
            
        if (self.left_dc > 100.0):
            self.left_dc = 100.0      
        if (self.left_dc < 0.0):
            self.left_dc = 0.0
            
        self.pwm0.ChangeDutyCycle(self.right_dc)
        self.pwm1.ChangeDutyCycle(self.right_dc)
        self.pwm2.ChangeDutyCycle(self.left_dc)
        self.pwm3.ChangeDutyCycle(self.left_dc)