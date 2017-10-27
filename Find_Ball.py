import Config
import sys
import cv2
import qi
import image
import time
import numpy as np
import math
import Obtain_Image

def look_down():
    """lower the pitch of head to look for ball that is at foot step   """
    print "Start Scanning Field"
    motion_service = Config.motion_service

    # rotate the HeadPitch joint to a lower angle
    name = "HeadPitch"
    angle = 0.45
    fractionMaxSpeed = 0.2
    motion_service.setAngles(name, angle, fractionMaxSpeed)
    # sleep for 0.5 secs to stabilize motion and avoid blurry pictures
    time.sleep(0.5)

def take_picture():
    Obtain_Image.Init_Camera(1)
    im = Obtain_Image.GetImage()
    im.show()
    im.save("Find_Ball.png", "PNG")

# def locate_ball():

def locate_Ball():
    img = cv2.imread("Find_Ball.png", 1)

    # cv2.namedWindow("HSV Image",cv2.CV_WINDOW_AUTOSIZE)
    # cv2.namedWindow("Binary Image",cv2.CV_WINDOW_AUTOSIZE)

    # cv2.namedWindow("dilate Image",cv2.CV_WINDOW_AUTOSIZE)
    # cv2.namedWindow("goal detected Image",cv2.CV_WINDOW_AUTOSIZE)

    print "Width of the image :" + str(img.shape[1])  # width
    print "Height of the image  :" + str(img.shape[0])  # height

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #cv2.imshow("HSV Image", hsv)

    blue = cv2.inRange(hsv, np.array([2, 100, 150], np.uint8), np.array([25, 255, 255], np.uint8))
    #cv2.imshow("Binary Image", blue)

    erode = cv2.erode(blue, None, iterations=1)
    #cv2.imshow("erode Image", erode)

    dilate = cv2.dilate(erode, None, iterations=5)
    #cv2.imshow("dilate Image", dilate)
    #cv2.waitKey()

    #######################################
    smoothing = cv2.blur(blue, (10, 10))
    dilate = cv2.dilate(smoothing, None, iterations=3)
    # storage=cv2.CreateMemStorage(0)
    # dilate=camImage.fromarray(dilate)
    # circles=cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,2,2.5,200,100,25,0)
    circles = cv2.HoughCircles(np.asarray(dilate), cv2.HOUGH_GRADIENT, 100, 300, 100, 50)
    ##########################################

    _, contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    print "Y-axis : Top to bottom"
    print "X-axis : Left to right"

    Cx, Cy, W, H, X, Y = 0, 0, 0, 0, 0, 0
    maxdiag = 0

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cx, cy = x + w / 2, y + h / 2
        # print "Center : (" + str(cx) + "," + str(cy) + ") , Width :" + str(w) + ", Height :" + str(h) + ", Radius = (Width+Height)/2 : " + str((w + h) / 2)
        if 20 < hsv.item(cy, cx, 0) < 30:
            cv2.rectangle(img, (x, y), (x + w, y + h), [0, 255, 255], 2)
        if (math.sqrt(w * w + h * h) > maxdiag):
            maxdiag = math.sqrt(w * w + h * h)
            Cx, Cy, W, H, X, Y = cx, cy, w, h, x, y

    cv2.rectangle(img, (X, Y), (X + W, Y + H), [0, 23, 255], 2)
    print "CENTER : (" + str(Cx) + "," + str(Cy) + ") , WIDTH :" + str(W) + ", HEIGHT :" + str(H)
    cv2.imshow('Ball detected Image', img)
    cv2.waitKey()

    forward = 0
    horizontal = 0
    use_left_kick = 0

    if (Cy < 130):
        print "move one step in front"
        forward= 1

    if(  Cx > 524   ):
        horizontal = 2
    if( Cx < 524 and Cx > 450   ):
        horizontal = 1
    if( Cx < 450 and Cx > 400  ):
        horizontal = 0.5
    if(Cx < 400 and Cx > 360):
        horizontal = 0

    if(Cx > 320 and Cx < 360):
        horizontal = -0.5
        use_left_kick = 1
    if(Cx < 130):
        horizontal = -2
        use_left_kick = 1
    if(Cx > 130 and Cx < 220):
        horizontal = -1
        use_left_kick = 1

    print [horizontal,forward , use_left_kick]

    x = 0.0
    y = -0.05
    theta = 0.0

    # parameters are set to the default value
    Config.motion_service.walkTo(x, y*horizontal , theta, [["StepHeight", 0.02]])  # step height of 4 cm

    return [horizontal , forward , use_left_kick]

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
    x = 0.0
    y = -0.00
    theta = 0.0

    # parameters are set to the default value
    Config.motion_service.walkTo(x, y, theta, [["StepHeight", 0.02]])  # step height of 4 cm

    look_down()
    take_picture()
    locate_Ball()