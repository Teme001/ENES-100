
from turtle import forward
import RPi.GPIO as GPIO # always needed with RPi.GPIO
import time
import socket
import cv2
import numpy
import pygame

pygame.display.init()
pygame.joystick.init()
pygame.joystick.Joystick(0).init()

SERVER_ADDRESS = 'Server Port'
SERVER_PORT = 88888


# Create the socket
c = socket.socket()
c.connect((SERVER_ADDRESS, SERVER_PORT))
c.listen(10)


print("Searching for address %s.To terminate the" +
       "program press Ctrl +c on PC or L1 +L2 on joystick" %
      str((SERVER_ADDRESS, SERVER_PORT)))

# This process will continue until it connects to a client.
# Once connected you will have full access 
# If disconnected it will revert to previous state and seach for client again
while True:
    
    
    c, addr = c.accept()
    print("\nConnection was successfull %s" % str(addr))
    
    FM_A = 26
    FM_B = 19
    BM_A = 13
    BM_B = 5
    F_PWM_PIN = 20
    B_PWM_PIN = 16
    



    #GPIO SETUP
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(FM_B, GPIO.OUT)
    GPIO.setup(FM_A, GPIO.OUT)
    GPIO.setup(F_PWM_PIN, GPIO.OUT)
    GPIO.setup(BM_A, GPIO.OUT)
    GPIO.setup(BM_B, GPIO.OUT)
    GPIO.setup(B_PWM_PIN, GPIO.OUT)

    F_FORWARD = GPIO.PWM(F_PWM_PIN, 1000)
    B_BACKWARD = GPIO.PWM(B_PWM_PIN, 1000)
    GPIO.output(B_PWM_PIN,GPIO.LOW)
    GPIO.output(F_PWM_PIN,GPIO.LOW)
     

    F_FORWARD.start(80)  
    B_BACKWARD.start(60)
 
   # B_PWM.ChangeDutyCycle(30)  

    while True:
        
        B_BACKWARD.ChangeDutyCycle(60) 
       
        data = c.recv(2048)
        if not data:
            print("End of file from client. Resetting")
            break

        # Decode the received bytes into a unicode string using the default
        # codec. (This isn't strictly necessary for python2, but, since we will
        # be encoding the data again before sending, it works fine there too.)
        data = str(data.decode())
        

        print("Received '%s' from client" % data)
        AY = int(data[0:3])
        BX = int(data[3:])
        
        
        if AY < 160:
                GPIO.output(BM_A,GPIO.HIGH)
                GPIO.output(BM_B,GPIO.LOW)
                
                print("FRONT")
        elif AY > 240:
                
                GPIO.output(BM_A,GPIO.LOW)
                GPIO.output(BM_B,GPIO.HIGH)
                print("BACK")
                
        else:
                GPIO.output(BM_A,GPIO.LOW)
                GPIO.output(BM_B,GPIO.LOW)
                print("NO F/B")

        if BX < 160:
                GPIO.output(FM_A,GPIO.HIGH)
                GPIO.output(FM_B,GPIO.LOW)
                B_BACKWARD.ChangeDutyCycle(60) 
                print("L")
        elif BX > 240:
                
                GPIO.output(FM_A,GPIO.LOW)
                GPIO.output(FM_B,GPIO.HIGH)
                B_BACKWARD.ChangeDutyCycle(60) 
                print("R")
        else :
                GPIO.output(FM_A,GPIO.LOW)
                GPIO.output(FM_B,GPIO.LOW)
                print("NO L/R")
        F_FORWARD.send()
        B_BACKWARD.send()
        F_FORWARD.stop()            # stop the PC output
        B_BACKWARD.stop() 

       

        bx = str(int((pygame.joystick.Joystick(0).get_axis(3)*100)+200))
        ay = str(int((pygame.joystick.Joystick(0).get_axis(1)*100)+200))
        data = ay + bx
        # Convert string to bytes. (No-op for python2)
        data = data.encode()

        # Send data to server
        c.send(data)
         # Receive response from server
        data = c.recv(2048)
        if not data:
            print("Server ended. Exiting")
            break
        print(data)
        

        # See above
        data ="200"
        data = data.encode()

        # Send the modified data back to the client.
        
        c.send(data)
        
        

          # stop the PWM output
        GPIO.cleanup()
        c.close()