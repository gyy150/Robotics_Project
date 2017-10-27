import qi
import sys

robotIp = "192.168.2.100"
PORT = 9559

print "----------------------Connecting to Nao-------------------------"
global session
session = qi.Session()
try:
    session.connect("tcp://" + robotIp + ":" + "9559")

    motion_service = session.service("ALMotion")
    cam_service    = session.service("ALVideoDevice")
    memory_service = session.service("ALMemory")

    posture_service = session.service("ALRobotPosture")
    posture_service.goToPosture("StandInit", 0.5)
    
except RuntimeError:
    print "Error: Cannot connect to NAO"
    sys.exit(1)

print "-------------------------Configuring Done------------------------------------------"