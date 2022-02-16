from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import requests
import json

import wget
import zipfile

from collections import deque


def downloadDriver():
    #get driver version
    url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
    resp = requests.get(url)
    driver_version = resp.text

    #download latest version of driver
    download_url = "https://chromedriver.storage.googleapis.com/" + driver_version +"/chromedriver_win32.zip"
    driver_zip = wget.download(download_url,'chromedriver.zip')

    extract_path = os.path.join(os.getcwd(), "Source")
    with zipfile.ZipFile(driver_zip, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    # delete zip file
    os.remove(driver_zip)

def getSeleniumAlign(youtubeID):

    #refresh driver if exists
    driver_path = os.path.join(os.getcwd(), "Source", "chromedriver.exe")
    if os.path.exists(driver_path):
        os.remove(driver_path)
    downloadDriver()

    #remove possible json.txt files
    timings_path = os.path.join(os.getcwd(), "Source", "TextFiles", "timings.json")
    if os.path.exists(timings_path):
        os.remove(timings_path)

    # open web browser
    try:
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        driver = webdriver.Chrome(driver_path, options=option)
        url = "https://autolyrixalign.hltnus.org/"
        driver.get(url)

        driver.implicitly_wait(6)
    except:
        success = False
        return success

    #get appropriate form elements
    form = driver.find_elements_by_class_name("audioForm")[0]
    text_input = driver.find_elements_by_name("lyrixs_file")[0]
    file_input = driver.find_elements_by_name("audio_file")[0]

    #give path of files to form
    music_path = os.path.join(os.getcwd(),"Source", "AudioFiles", f"{youtubeID}.mp3")
    text_path = os.path.join(os.getcwd(), "Source", "TextFiles", f"{youtubeID}.txt")
    text_input.send_keys(text_path)
    file_input.send_keys(music_path)
    form.submit()

    #wait until browser redirects i.e. completes action 
    wait = WebDriverWait(driver, 1000)
    wait.until(lambda driver: driver.current_url != url)

    #download and save json data to txt file
    json_href = driver.find_elements_by_id("downloadJsonLyrix")[0].get_attribute('href')
    resp = requests.get(json_href)
    text = resp.text

    json_text = json.loads(text)
    flattened_json = []
    for line in json_text:
        if len(line) != 0:
            for entry in line:
                if (entry['text'] != 'BREATH*'):
                    element = {}
                    element['key'] = entry['text']
                    element['start'] = float(entry['start'])
                    element['duration'] = float(entry['end']) - float(entry['start'])
                    flattened_json.append(element)
    
    with open(timings_path, 'w') as f:
        json.dump(flattened_json, f)

    #close driver
    driver.quit()

    success = True
    return success


def validateJson(youtubeID):

    # find path of text file and load into json format
    text_path = os.path.join(os.getcwd(), "Source", "TextFiles")
    with open (os.path.join(text_path, "timings.json"), 'r') as f:
        text_json = json.load(f)
    
    #get known words to compare
    with open (os.path.join(text_path, f"{youtubeID}.txt"), 'r') as f:
        original_text = f.read().upper()
    
    #cylce through all returned words and detect if the returned transcript matches
    unknown_word_found = False
    for entry in text_json:
        if entry['key'] not in original_text and entry['key'] != "BREATH*":
            unknown_word_found = True

    # if there is an unkown word then selenium has returned wrong transcipt
    return unknown_word_found

def trimTimings(keywords, song_duration, buffer):

    #get all timings
    text_path = os.path.join(os.getcwd(), "Source", "TextFiles")
    with open (os.path.join(text_path, "timings.json"), 'r') as f:
        text_json = json.load(f)

    timed_json = []
    for entry in keywords:
        split_keyword = entry.split()
        d = deque(maxlen=len(split_keyword))
        for elem in text_json:
            d.append(elem)
            if len(d)==len(split_keyword) and d[0]['key'].lower() == split_keyword[0].lower():
                possible_match = True
                for d_item, key_item in zip(d, split_keyword):
                    if d_item['key'].lower() != key_item.lower():
                        possible_match = False
                        break
                if possible_match:
                    element = {}
                    element['key'] = entry
                    element['start'] = d[0]['start']
                    element['duration'] = sum(item['duration'] for item in d)
                    timed_json.append(element)

    timed_json.sort(key=lambda entry: entry['start'])

    # add buffer to prolong image
    previous_start_end = None

    for i in range(len(timed_json)):
        start = timed_json[i]['start']
        end = timed_json[i]['start'] + timed_json[i]['duration']

        possible_start = start - buffer
        if i == 0:
            #if first must only not be befor zero
            if possible_start < 0:
                possible_start = 0
                timed_json[i]['start'] = possible_start
            else:
                timed_json[i]['start'] = possible_start
        else:
            # if not first then must also not conlict with previous
            previous_end = timed_json[i-1]['start'] + timed_json[i-1]['duration']
            if possible_start > 0 or possible_start > previous_end:
                timed_json[i]['start'] = possible_start

        if (i+1) < len(timed_json):
            # need to look at next one not to over-lap
            next_start = timed_json[i+1]['start'] - buffer
            possible_end = end + buffer
            if possible_end < next_start:
                timed_json[i]['duration'] = possible_end - possible_start 
            else:
                timed_json[i]['duration'] = next_start - possible_start
        else:
            #no next one, check doesn't conflict with end of song
            if possible_end < song_duration:
                timed_json[i]['duration'] = possible_start - possible_end
            else:
                timed_json[i]['duration'] = possible_start - song_duration

    return timed_json
    