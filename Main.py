import Config
import Find_Goal
import Find_Ball
import Left_Kick
import Right_Kick
import time
import numpy as np
import math

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

    angle = Find_Goal.scan_field()

    motion = Config.motion_service

    motion.moveTo(0.0, 0.0, angle)
    time.sleep(2)

    Find_Ball.look_down()
    Find_Ball.take_picture()
    a = Find_Ball.locate_Ball()
    if(a[2]):
        Left_Kick.left_kick()
    else:
        Right_Kick.right_kick()

