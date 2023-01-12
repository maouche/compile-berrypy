import requests
import json
import os
import subprocess
import time
import sys
from getmac import get_mac_address as gma

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



def getAds(url, listVideos):
    return requests.post(
		url,
		verify=False,
		data=json.dumps(listVideos),
		headers={
			'mac': gma(),
			'Content-type': 'application/json'
		}
	)

def download(localTempPath, url, file):
    command = "wget -c --retry-connrefused --waitretry=3 --read-timeout=20 --timeout=15 -O " + localTempPath + str(file.id) + "_" + file.name + " " + url
    subprocess.call(command, shell=True)


def convertFile(localVideosPath, localTempPath, file):
    inputFile = localTempPath + str(file.id) + "_" + file.name

    # outputH264 = localVideosPath + str(file.id) + "_" +  os.path.splitext(file.name)[0] + ".h264"
    outputMP4 = localVideosPath + str(file.id) + "_" +  os.path.splitext(file.name)[0] + ".mp4"

    file_extension = os.path.splitext(file.name)[1]


    try:
        if (file_extension == ".jpg") or (file_extension == ".jpeg") or (file_extension == ".png") or (file_extension == ".gif") or (file_extension == ".webp"):
            subprocess.call("ffmpeg -y -loop 1 -i " + inputFile + " -s 1280x720 -c:v libx264 -t 5 -pix_fmt yuv420p " + outputMP4, shell=True)
            # subprocess.call("ffmpeg -y -i " + inputFile + " -vcodec copy " + outputH264, shell=True)
        else:
            subprocess.call("ffmpeg -y -i " + inputFile + " -vcodec copy " + outputMP4, shell=True)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

    finally:
        time.sleep(1)