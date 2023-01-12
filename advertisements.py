import api
from pathlib import Path
import os
import time
import sys


class File:
    def __init__(self, id, name):
        self.id = id
        self.name = name


def controller(localVideoPath, localTempPath, listVideos, host, clientCode):
    try:
        urlAds = host + "promotions/" + clientCode
        data = api.getAds(urlAds, listVideos).json()

        dowloadFiles(localVideoPath, localTempPath, data, host, clientCode)

        for f in data["filesToDelete"]:
            file = File(f["advertId"], f["fileName"])
            pathVideoFile = Path(localVideoPath + str(file.id) + "_" + os.path.splitext(file.name)[0] + ".mp4")
            pathTempFile = Path(localTempPath + str(file.id) + "_" + file.name)
            
            # if files exist
            if pathVideoFile.is_file():
                os.remove(localVideoPath + str(file.id) + "_" + os.path.splitext(file.name)[0] + ".mp4")
            if pathTempFile.is_file():
                os.remove(localTempPath + str(file.id) + "_" + file.name)

    
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)



def dowloadFiles(localVideoPath, localTempPath, data, host, clientCode) :
    filesToDownload = []  
    for f in data["filesToDownload"]:

        file = File(f["advertId"], f["fileName"])
        pathVideoFile = Path(localVideoPath + str(file.id) + "_" + os.path.splitext(file.name)[0] + ".mp4")
        pathTempFile = Path(localTempPath + str(file.id) + "_" + file.name)
        
        # if not file exist downloaded
        if pathTempFile.is_file() == False or pathVideoFile.is_file() == False:
        	filesToDownload.append(file)

    for file in filesToDownload:
        url = host + "promotions/" + clientCode + "/download/" + str(file.id)
        api.download(localTempPath, url, file)
        api.convertFile(localVideoPath, localTempPath, file)