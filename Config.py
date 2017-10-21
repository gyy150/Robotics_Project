import qi
import sys

robotIp = "192.168.2.112"
PORT = 9559

print "haha"
global session
session = qi.Session()
try:
    session.connect("tcp://" + robotIp + ":" + "9559")

    motion_service = session.service("ALMotion")
    cam_service = session.service("ALVideoDevice")

    posture_service = session.service("ALRobotPosture")
    posture_service.goToPosture("StandInit", 0.5)
    
except RuntimeError:
    print "Error: Cannot connect to NAO"
    sys.exit(1)

