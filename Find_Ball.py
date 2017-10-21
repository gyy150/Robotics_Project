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
    look_down()
    take_picture()