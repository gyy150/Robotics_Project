import Config
import time
import qi
import argparse
import sys
import math
import motion as mot
from naoqi import ALProxy
import vision_definitions
from PIL import Image

def Init_Camera(IP, PORT,camera_id):
    global camProxy
    camProxy = Config.session.service("ALVideoDevice")
    camProxy.setActiveCamera(camera_id)

    #print 'camera parameters adjustment:'
    #camindex = camProxy.getCameraIndexes()
    #print type(camindex[0])

    print camProxy.getParameter(1 , vision_definitions.kCameraBrightnessID )
    brightness = camProxy.getParameterRange(1 , vision_definitions.kCameraBrightnessID )
    print brightness

    print camProxy.getParameter(1 , vision_definitions.kCameraSaturationID )
    print camProxy.getParameterRange(1 , vision_definitions.kCameraSaturationID )
    
    camProxy.setParameter(1 , vision_definitions.kCameraBrightnessID , ( brightness[1] - brightness[0] )/2 )


     

def GetImage():
    resolution = vision_definitions.kVGA
    colorSpace = vision_definitions.kYUVColorSpace
    
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
    
    sb = str(array )

    #im = Image.fromstring("RGB", (imageWidth, imageHeight), sb)
    #sb = buffer(array, 0 , len(array) )    
    #print len(array)
    #s = ''
    #for value in array:
    #    s+= ' ' + str(value)

    #print s
    
  # Create a PIL Image from our pixel array.

    im = Image.frombytes( "RGB" ,  (imageWidth, imageHeight), sb )

#    im = Image.frombytes(array, decoder_name='raw', arg  )

  # Save the image.
    

    return im


if __name__ == "__main__":


    robotIp = "192.168.2.121"
    PORT = 9559
    session = qi.Session()
    try:
        session.connect("tcp://" + robotIp + ":" + "9559")
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    Init_Camera(robotIp , PORT  , 1)
    GetImage()
