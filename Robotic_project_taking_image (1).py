import sys
import time
import numpy as np
# Python Image Library
from PIL import Image

from naoqi import ALProxy
import cv2
import config
import math
import find_goal
def showNaoImage(IP, PORT):
  """
  First get an image from Nao, then show it on the screen with PIL.
  """

  camProxy = ALProxy("ALVideoDevice", IP, PORT)
  resolution = 2    # VGA
  colorSpace = 11   # RGB

  videoClient = camProxy.subscribe("python_client", resolution, colorSpace, 5)

  t0 = time.time()

  # Get a camera image.
  # image[6] contains the image data passed as an array of ASCII chars.
  naoImage = camProxy.getImageRemote(videoClient)

  t1 = time.time()

  # Time the image transfer.
  print "acquisition delay ", t1 - t0

  camProxy.unsubscribe(videoClient)


  # Now we work with the image returned and save it as a PNG  using ImageDraw
  # package.

  # Get the image size and pixel array.
  imageWidth = naoImage[0]
  imageHeight = naoImage[1]
  array = naoImage[6]

  # Create a PIL Image from our pixel array.
  #im = Image.fromstring("RGB", (imageWidth, imageHeight), array)
  im = Image.frombytes("RGB", (imageWidth, imageHeight), array)

  # Save the image.
  im.save("camImage.png", "PNG")
  im=Image.open("camImage.png")
  im.mode
  'p'
  im=im.convert('RGB')
  im.mode
  'RGB'
  im.save('camImage_asjpg.jpg',quality=95)
  im.show()

def findgoal():
	img = cv2.imread("camImage.png",1)
	
	
	print "Width of the image :" + str(img.shape[1]) #width
	print "Height of the image :" + str(img.shape[0]) #height
	 
	hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	cv2.imshow("HSV Image", hsv)

	lower_yellow=np.array((0,100,80),np.uint8)
	higher_yellow=np.array((180,255,255),np.uint8)
	yellow = cv2.inRange(hsv,lower_yellow, higher_yellow)
	cv2.imshow("Binary Image", yellow)
	
	erode = cv2.erode(yellow,None,iterations = 2)
	cv2.imshow("erode Image", erode)
	
	dilate = cv2.dilate(erode,None,iterations = 3)
	cv2.imshow("dilate Image", dilate)
	
	
#	contours,hierarchy = cv2.findContours(dilate,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
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

def take_position():
	
    motionProxy = config.loadProxy("ALMotion")

    # Set NAO in stiffness On
    config.StiffnessOn(motionProxy)
    D = find_goal.findgoal()
    theta = math.atan(D/120.0)

    x     = 0.30*(1 - math.cos(theta))
    y     = -0.30*(math.sin(theta))
    print x,y,theta 
    if D > 30.0 or D < -(30.0) :
        theta =   math.atan(D/120.0)
        motionProxy.walkTo(x, y, theta)


if __name__ == '__main__':
  IP = "192.168.2.121"              # IP add
  PORT = 9559

  # Read IP address from first argument if any.
  if len(sys.argv) > 1:
    IP = sys.argv[1]

  naoImage = showNaoImage(IP, PORT)
  detectedImage = findgoal()
  take_position(30,30,60)
