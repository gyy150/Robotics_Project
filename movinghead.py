

import qi
import argparse
import sys
import time


def main(session):
    motion_service  = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

   
    posture_service.goToPosture("StandInit", 0.5)


    names  = ["HeadYaw","HeadPitch"]

    angleLists  = [[1.08, .508, 0, -0.508, -1.08], [-0.50, -0.32, 0, 0.32, 0.20]]
    timeLists   = [[2.0, 4.0, 6.0, 8.0, 10.0], [2.0, 4.0, 6.0, 8.0 ,10.0 ]]
    isAbsolute  = True
    motion_service.angleInterpolation(names, angleLists, timeLists, isAbsolute)

    time.sleep(1.0)

    
    posture_service.goToPosture("StandInit", 0.5)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.2.100",
                        help="Robot IP address. On robot or Local Naoqi: use '192.168.2.127'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)
