import time
import qi
import argparse
import sys
import math
import motion as mot
from naoqi import ALProxy


def main(session):
    
    motion = session.service("ALMotion") 
    memory = session.service("ALMemory")

    while(True):
        print motion.getSummary()
        print "Left foot sensors values are:"
        print  memory.getData("Device/SubDeviceList/LFoot/FSR/FrontLeft/Sensor/Value")
        print  memory.getData("Device/SubDeviceList/LFoot/FSR/FrontRight/Sensor/Value")
        print  memory.getData("Device/SubDeviceList/LFoot/FSR/RearLeft/Sensor/Value")
        print  memory.getData("Device/SubDeviceList/LFoot/FSR/RearRight/Sensor/Value")




if __name__ == "__main__":


    robotIp = "192.168.2.115"
    PORT = 9559
    session = qi.Session()
    try:
        session.connect("tcp://" + robotIp + ":" + "9559")
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)
