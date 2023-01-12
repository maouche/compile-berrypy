#import sys
#sys.path.insert(0, '/usr/local/lib/python3.9/site-packages/')

import cv2
import screeninfo
import time
import numpy as np




def initScreen(window_name):
    # get the size of the screen
   screen = screeninfo.get_monitors()[0]
   
   # setting screen
   cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
   cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
   cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)





def play(localVideoPath, listVideos, window_name):
   index = 0
   capture = cv2.VideoCapture(localVideoPath + "/" + listVideos[index])
   isFinished = False
   
   

   if (capture.isOpened() == False):
      print("Error Opening Video Stream Or File")

  
   while (capture.isOpened()):
      if isFinished :

         index = index + 1
         if index != len(listVideos) :
            capture.open(localVideoPath + "/" + listVideos[index])
            isFinished = False
         else:
            break
         


      ret, frame = capture.read()

      if ret == True:
         
         
         frameResized = rescale_frame(frame)
         
         
         
         cv2.imshow(window_name, frameResized)

         if cv2.waitKey(25) == ord('q'):
            return "q"
            break
      else:
         isFinished = True




def rescale_frame(frame):
      # get the size of the screen
      screen = screeninfo.get_monitors()[0]
      width, height = screen.width, screen.height
      dim = (width, height)
      return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)
