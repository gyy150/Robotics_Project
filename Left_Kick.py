import Config
import qi
import argparse
import sys
import math
import motion as mot
from naoqi import ALProxy


def left_kick():
    
    motion = Config.motion_service
    posture = Config.posture_service
    
    memory = Config.memory_service

    posture.goToPosture("StandInit", 0.5)
#-----------------------------------
    TO_RAD = math.pi/180

    # Angle values
    kneeAngle  = 40
    torsoAngle =  0
    wideAngle  =  0

    #----------------------------- prepare the angles -----------------------------
    # Get the Number of Joints
    NumJoints = len(motion.getJointNames("Body"))

    # Define The Initial Position
    Head     = [0, 0]
    LeftArm  = [120,  15, -90, -80]
    LeftLeg  = [0,  wideAngle, -kneeAngle/2-torsoAngle, kneeAngle, -kneeAngle/2, -wideAngle]
    RightLeg = [0, -wideAngle, -kneeAngle/2-torsoAngle, kneeAngle, -kneeAngle/2,  wideAngle]
    RightArm = [120, -15,  90,  80]

    # If we have hands, we need to add angles for wrist and hand
    if (NumJoints == 26):
        LeftArm  += [0, 0]
        RightArm += [0, 0]

    # Gather the joints together
    pTargetAngles = Head + LeftArm + LeftLeg + RightLeg + RightArm

    # Convert to radians
    pTargetAngles = [ x * TO_RAD for x in pTargetAngles]

    #------------------------------ send the commands -----------------------------

    # Display the starting position
    print motion.getSummary()
    print "Left foot sensors values are:"
    print  memory.getData("Device/SubDeviceList/LFoot/FSR/FrontLeft/Sensor/Value")
    print  memory.getData("Device/SubDeviceList/LFoot/FSR/FrontRight/Sensor/Value")
    print  memory.getData("Device/SubDeviceList/LFoot/FSR/RearLeft/Sensor/Value")
    print  memory.getData("Device/SubDeviceList/LFoot/FSR/RearRight/Sensor/Value")

    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"

    # We set the fraction of max speed
    pMaxSpeedFraction = 0.2

    # Ask motion to do this with a blocking call
    motion.angleInterpolationWithSpeed(pNames, pTargetAngles, pMaxSpeedFraction)


    
    # Display the end position
    print motion.getSummary()
    print motion.getSummary()
    print "Left foot sensors values are:"
    print  memory.getData("Device/SubDeviceList/LFoot/FSR/FrontLeft/Sensor/Value")
    print  memory.getData("Device/SubDeviceList/LFoot/FSR/FrontRight/Sensor/Value")
    print  memory.getData("Device/SubDeviceList/LFoot/FSR/RearLeft/Sensor/Value")
    print  memory.getData("Device/SubDeviceList/LFoot/FSR/RearRight/Sensor/Value")

    motion.closeHand('RHand')



    TO_RAD = math.pi/180

    useSensors = False

    space      = mot.FRAME_ROBOT
    axisMask   = 63                     # control all the effector's axes
    isAbsolute = False

    times = 0.8
    LeftArm  = [90,  25, -90, -10]		# shoulder pitch/roll, elbow yaw/roll
    LeftArm	 = [ x * TO_RAD for x in LeftArm]

    RightArm = [90, -25,  90,  10]
    RightArm = [ x * TO_RAD for x in RightArm]

    motion.angleInterpolation(["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]
                              ,LeftArm+RightArm
                              ,times
                              ,True
                              ,_async=True) # "post" means non-blocking, so...

    effector   = "Torso"
    path       = [-0.001, -0.07, -0.01, 0.0, 0.0, 0.0]
    motion.positionInterpolation(effector, space, path, axisMask, 1.6, isAbsolute)

    space      = mot.FRAME_TORSO
    
    ### Swing left leg back
    # Move left arm to the front, right arm to the back
    times      = 0.5     
    effector   = "LLeg"         
    LeftArm  = [61,  25, -90, -10]
    LeftArm = [ x * TO_RAD for x in LeftArm]

    RightArm = [119, -25,  90,  10]
    RightArm = [ x * TO_RAD for x in RightArm]

    motion.angleInterpolation(
                                    ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]
                                    ,LeftArm+RightArm
                                    ,times
                                    ,True
                                    ,_async=True
                                    )

    path       = [-0.10, 0.00, 0.04, 0.0, 0.0, 0.0]

    motion.positionInterpolation(effector, space, path,
                                      axisMask, times, isAbsolute)
                                      



    ### Swing left leg forward
    # Move left arm all the way back, right arm to the front (but not all the way)
    times      = 0.3              
    LeftArm  = [119,  25, -90, -10]
    LeftArm = [ x * TO_RAD for x in LeftArm]

    RightArm = [61, -25,  90,  10]
    RightArm = [ x * TO_RAD for x in RightArm]

    motion.angleInterpolation(["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]
                              , LeftArm+RightArm
                              , times
                              , True
                              ,_async=True
                              )

    path       = [0.20, 0.0, 0, 0.0, 0.0, 0]

    motion.positionInterpolation(effector, space, path,
                                      axisMask, times, isAbsolute)

    posture.goToPosture("StandInit", 0.5)

##    # Move arms so they are facing straight down again
##    times      = 1.0                
##    LeftArm  = [90,  25, -90, -10]
##    LeftArm = [ x * TO_RAD for x in LeftArm]
##
##    RightArm = [90, -25,  90,  10]
##    RightArm = [ x * TO_RAD for x in RightArm]
##
##    motion.angleInterpolation(["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]
##                              , LeftArm+RightArm
##                              , times
##                              , True
##                              ,_async=True
##                              )
##    
##    path       = [-0.10, 0.0, -0.04, 0.0, 0.0, 0]
##    effector   = "LLeg"
##    motion.positionInterpolation(effector, space, path,
##                                      axisMask, 1.9, isAbsolute,_async=True
##                              )
##
##    effector   = "Torso"
##    path       = [0.001, 0.04, 0.01, 0.0, 0.0, 0.0]
##    motion.positionInterpolation(effector, space, path, axisMask, 2.5, isAbsolute)
    



      



#    while(1):
#        print("haha")


if __name__ == "__main__":


    # robotIp = "192.168.2.112"
    # PORT = 9559
    # session = qi.Session()
    # try:
    #   session.connect("tcp://" + robotIp + ":" + "9559")
    # except RuntimeError:
    #    print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
    #           "Please check your script arguments. Run with -h option for help.")
    #    sys.exit(1)

    left_kick()
