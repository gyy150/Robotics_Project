import Config
import sys
import cv2
import qi
import image
import time
import numpy as np
import math
import Obtain_Image


def Scan_Field():
    print "Start Scanning Field"
    motion_service  = Config.session.service("ALMotion")

    Obtain_Image.Init_Camera(Config.robotIp, Config.PORT, 0 )

    #set the head to face the centre
    names  = ["HeadYaw", "HeadPitch"]
    angles  = [0.0, 0.0]
    fractionMaxSpeed  = 0.2
    motion_service.setAngles(names, angles, fractionMaxSpeed)

    #retotate the head to sacn the field
    name = "HeadYaw"
#    angleLists  = [1.08, .508, 0, -0.508, -1.08]
##    timeLists   = [2.0, 4.0, 6.0, 8.0, 10.0]
##    isAbsolute  = True
##    motion_service.angleInterpolation(name, angleLists, timeLists, isAbsolute)

    rotation_range = 2.16
    number_of_division = 10
    increment = rotation_range / number_of_division
    
    for i in range(number_of_division+1):
        angle = -1.08 + increment * i
        motion_service.setAngles(name, angle, fractionMaxSpeed)
        print "Looking at angle:" + str(angle)
        im = Obtain_Image.GetImage()
        #im.show()
        picture_name = "camImage"+str(angle) + ".PNG"
        im.save( picture_name , "PNG")

        findgoal(picture_name)

        time.sleep(2.0)
        

    #reset the head to initial position    
    angles  = [0.0, 0.0]
    fractionMaxSpeed  = 0.2
    motion_service.setAngles(names, angles, fractionMaxSpeed)
    
    print "Finished Scanning Field"
def findgoal( picture_name):
    
    img = cv2.imread( picture_name ,  cv2.IMREAD_COLOR  )
##    print "Width of the image :" + str(img.shape[1]) #width
##    print "Height of the image :" + str(img.shape[0]) #hight
##
##    #grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
##    cv2.imshow('gray_image',img)
##    cv2.waitKey(0)
##    
##    img = cv2.GaussianBlur(img,(5,5),0)
##    ret2,binary = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
##    cv2.imshow('binary_image',binary)
##    cv2.waitKey(0)
##
##
##    contours,hierarchy , _ = cv2.findContours( binary,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
##
    #convert the BGR image to HSV format
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    cv2.imshow("HSV Image", hsv)

    #create numpy array representing the range of HSV value
    lower_yellow=np.array((0,100,80),np.uint8)
    higher_yellow=np.array((180,255,255),np.uint8)

    #use cv2.inRange function to extract thee yellow part of the picture
    yellow = cv2.inRange(hsv,lower_yellow, higher_yellow)
    cv2.imshow("Binary Image", yellow)

    #erosion and dilation to bring the segmented image together
    erode = cv2.erode(yellow,None,iterations = 2)
    cv2.imshow("erode Image", erode)
	
    dilate = cv2.dilate(erode,None,iterations = 3)
    cv2.imshow("dilate Image", dilate)

    #
    _,contours,hierarchy = cv2.findContours(dilate,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	
    print "Y-axis : Top to bottom"
    print "X-axis : Left to right"
	
    Cx,Cy,W,H,X,Y=0,0,0,0,0,0
	
    maxdiag=0
	
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        cx,cy = x+w/2, y+h/2
        print "Center : ("+ str(cx)+","+str(cy)+") , Width :"+str(w)+", Height :"+str(h)+", Diameter = (Width+Height)/2 : "+str((w+h)/2)
        cv2.rectangle(img,(x,y),(x+w,y+h),[0,255,255],2)
    
        if (math.sqrt(w*w+h*h)>maxdiag) :
            maxdiag=math.sqrt(w*w+h*h)
            Cx,Cy,W,H,X,Y=cx,cy,w,h,x,y
		
	
	    
    cv2.rectangle(img,(X,Y),(X+W,Y+H),[0,23,255],2)
    print "CENTER : ("+ str(Cx)+","+str(Cy)+") , WIDTH :"+str(W)+", HEIGHT :"+str(H)
	
    y=120 ### Set the value of y over here
	
    Distance= ((y*0.5773)/160)*(160-Cx)
	
    print "Estimated real distance 'x' from the line y to the center of the goal is = "+str(Distance)
    cv2.imshow('goal detected Image',img)
    cv2.waitKey()
    return Distance







if __name__ == "__main__":

##    robotIp = "192.168.2.121"
##    PORT = 9559
##    session = qi.Session()
##    try:
##        session.connect("tcp://" + robotIp + ":" + "9559")
##    except RuntimeError:
##        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
##               "Please check your script arguments. Run with -h option for help.")
##        sys.exit(1)
    Scan_Field()
    
