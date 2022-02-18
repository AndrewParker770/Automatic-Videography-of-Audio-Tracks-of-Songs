import json
import requests
import sys
import os
import shutil

import imghdr

from bs4 import BeautifulSoup

from PIL import Image
import numpy as np
import cv2


def getGoogleImage(word):
    #refines google search a little to exclude titles of media/products etc
    exclude_search = ["-movie", "-books", "-TV", "-product"]
    #manage if "word" is more than one word
    keyword_list = word.split(" ")
    whole_list = keyword_list + exclude_search
    search_string = "+".join(whole_list)

    file_name = "-".join(keyword_list)

    url = "https://www.google.com/search?hl=jp&q=" + search_string + "&btnG=Google+Search&tbs=0&safe=off&tbm=isch"
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",}

    response = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    os.makedirs(f'videography/static/imgs/{file_name}')

    images = soup.find_all("img", {"class": "yWs4tf"})

    counter = 0
    for source in images:  
        if counter > 5:
            break

        img_data = requests.get(source['src']).content
        with open(f'videography/static/imgs/{file_name}/{counter}.jpeg', 'wb') as handler:
            handler.write(img_data)

        image = Image.open(f'videography/static/imgs/{file_name}/{counter}.jpeg')
        if len(np.array(image).shape) == 3:
            counter += 1


def deleteFiles(folders):
    endings = [".txt", ".mp4", ".mp3", ".png"]
    
    for folder in folders:
        for filename in os.listdir(folder):
            name, file_extension = os.path.splitext(filename)
            if (file_extension in endings):
                os.unlink(os.path.join(folder, filename))

def deleteDirs(folders):
    for folder in folders:
        for filename in os.listdir(folder):
            if (os.path.isdir(os.path.join(folder, filename))):
                shutil.rmtree(os.path.join(folder, filename))





def extractFrames(youtubeID):
    if not os.path.exists('Source/FrameFiles'):
        os.makedirs('Source/FrameFiles')
    
    video = cv2.VideoCapture(f"Source/VideoFiles/{youtubeID}.mp4")
    fps = video.get(cv2.CAP_PROP_FPS)

    path = 'Source/FrameFiles'
    ret, frame = video.read()
    index = 0
    name = f'{path}/frame{index}.png'
    index += 1
    cv2.imwrite(name, frame)

    while ret:
        ret, frame = video.read()
        if (ret and (index % int(fps//2) == 0)):
            name = f'{path}/frame{index}.png'
            cv2.imwrite(name, frame)
        
        index +=1

    video.release()
    cv2.destroyAllWindows()

    return fps