import qi
import sys

robotIp = "192.168.2.112"
PORT = 9559

print "haha"
global session
session = qi.Session()
try:
    session.connect("tcp://" + robotIp + ":" + "9559")
    posture_service = session.service("ALRobotPosture")
    posture_service.goToPosture("StandInit", 0.5)
    
except RuntimeError:
    print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
    sys.exit(1)
