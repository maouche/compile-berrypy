#import sys
#sys.path.insert(0, '/usr/local/lib/python3.9/site-packages/')
import player
import os
import pyautogui
import advertisements
import threading
import cv2
import time 


localTempPath = './temp/'
localVideosPath = './videos/'
window_name = 'BerryBox Player'



runScreen = False
stop_threads = False




# Hide MOUSE
pyautogui.FAILSAFE = False
pyautogui.moveTo(0, 0) 






# Get url in url.txt
                                
host = ''
content = ''
with open('url.txt') as f:
    content = f.readlines()
    f.close()
host = content[0]
                                




# Get Code client in code.txt
                                
clientCode = ''
with open('code.txt') as f:
    content = f.readlines()
    f.close()
clientCode = content[0]
                                





# To create repositories if not exist
                                                  
def iniRepositories():
    if not os.path.exists(localTempPath):
        os.makedirs(localTempPath)
    if not os.path.exists(localVideosPath):
        os.makedirs(localVideosPath)
                                                  
iniRepositories()








# Function to Donwload and Convert Image and Video to MP4 video
                                                                                                
def loopdownloadandconvert():
    global stop_threads

    while True:
        if stop_threads:
            break

        # get list videos
        listVideos = os.listdir(localVideosPath)

        # Download and convert videos
        advertisements.controller(localVideosPath, localTempPath, listVideos, host, clientCode)
        time.sleep(60)
                                                                                                










# function to Read all videos and show it in Screen with OpenCV
                                                                            
def loopreadvideos():
    global runScreen
    global stop_threads
    global thread1
    global thread2

    while True:
        if stop_threads:
            break

        # get list videos
        listVideos = os.listdir(localVideosPath)

        # Read videos
        if len(listVideos) > 0:

            if (runScreen == False):
                # Init Screen
                player.initScreen(window_name)
                runScreen = True

            # # Play list videos
            play = player.play(localVideosPath, listVideos, window_name)
            if (play == "q"):
                stop_threads = True
                                                                            




# Run Two Processors
thread1 = threading.Thread(target=loopreadvideos)
thread1.start()
                                                                            
thread2 = threading.Thread(target=loopdownloadandconvert)
thread2.start()

                                                                            
                                                                            
