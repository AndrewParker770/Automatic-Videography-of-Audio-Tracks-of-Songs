import requests
import json
import requests
import sys
import os
import shutil

import imghdr

from bs4 import BeautifulSoup
import wikipedia

from pil import Image

WIKI_REQUEST = 'https://en.wikipedia.org/wiki/'

def get_wiki_images(search_term):
    try:
        result = wikipedia.search(search_term, results = 1)
        wikipedia.set_lang('en')
        wkpage = wikipedia.WikipediaPage(title = result[0])
        title = wkpage.title
    except:
        print("failed")
        return 0

    url = WIKI_REQUEST + title

    response  = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    sources = []

    # find potential sources in thumbdivs
    thumbdivs = soup.find_all("div", {"class": "thumbinner"})
    for div in thumbdivs:
        if title.lower() in div.get_text().lower():
            images = div.find_all("a", {"class": "image"})
            for image in images:
                sources.append((image.find("img"))['src'])

    # find potential sources in the sidebar
    infoSidebar = soup.find_all("table", {"class": "sidebar"})
    for info in infoSidebar:
        if title.lower() in info.get_text().lower():
            images = info.find_all("a", {"class": "image"})
            for image in images:
                sources.append((image.find("img"))['src'])

    # find potential sources in info tables (i.e. a class for divs in wikipedia)
    infoTable = soup.find_all("table", {"class": "infobox"})
    for info in infoTable:
        if title.lower() in info.get_text().lower():
            images = info.find_all("a", {"class": "image"})
            for image in images:
                sources.append((image.find("img"))['src'])
    
    # find images in thumb classes
    thumbDiv = soup.find_all("div", {"class": "gallerybox"})
    for thumb in thumbDiv:
        if title.lower() in thumb.get_text().lower():
            images = thumb.find_all("a", {"class": "image"})
            for image in images:
                sources.append((image.find("img"))['src'])
    
    printSources(sources, title, 5)

def deleteFiles(folders):
    for folder in folders:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Error: Unable to delete %s.' % (file_path))
    

def printSources(sources, title, MAX_DOWNLOAD):
    counter = 0

    parentPath = os.getcwd()
    
    os.mkdir(os.path.join(os.path.join(os.getcwd(), 'videography/static/imgs'), title))
    os.chdir(os.path.join(os.path.join(os.getcwd(), 'videography/static/imgs'), title))
    for source in sources:
        if counter > MAX_DOWNLOAD:
            break
        url = 'https:' + source
        img_data = requests.get(url).content
        with open(f'{counter}.png', 'wb') as handler:
            handler.write(img_data)
        
        try:
            # check png is valid and increment if so
            image = Image.open(f'{counter}.png')
            counter += 1
        except:
            # delete broken file
            os.remove(f'{counter}.png')
    os.chdir(parentPath)

def performImageSearch(searchTerms):
    for term in searchTerms:
        get_wiki_images(term)
