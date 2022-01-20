import sys
import os
import yake
import re
import pytesseract

from youtube_transcript_api import YouTubeTranscriptApi
from PIL import Image

def getKeywords(youtubeID):
    
    #get all lines from .txt file
    with open(f"Source/TextFiles/{youtubeID}.txt", "r") as f:
        lines = f.read().splitlines() 
        
    #find a single key word in each lne
    keywords = set([])
    for line in lines:
        result = returnKeyWords(line, 1)
        if result != []:
            keywords.add(result[0][0].lower())
    return keywords



def getCaptions(youtubeID, fakeYoutubeID):
    transcript_dict = YouTubeTranscriptApi.get_transcripts([youtubeID], languages=['en'])
    with open(f"Source/TextFiles/{fakeYoutubeID}.txt", "w") as f:
        for line in transcript_dict[0][youtubeID]:
            raw_line = line['text']
            #remove non_ASCII chars
            encoded_text = raw_line.encode("ascii", "ignore")
            text = encoded_text.decode()
            #remove newline chars and re-add
            text = text.replace("\n", " ")
            if text[-1] != '\n':
                text += '\n'
            f.write(text)
    return os.path.exists(f"Source/TextFiles/{fakeYoutubeID}.txt"), transcript_dict[0][youtubeID]
        
    
def flattenTranscript(transcript):
    wholeTranscript = ''
    for line in transcript[0][youtubeLinkID]:
        wholeTranscript += (line['text'] + ' ') 
    return wholeTranscript

def returnKeyWords(text, numOfKeywords):
    
    language = "en"
    max_ngram_size = 2
    deduplication_thresold = 0.9
    deduplication_algo = 'seqm'
    windowSize = 2

    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(text)

    return keywords

def getLyricTranscript(keywords, fps):

    myconfig = r"--psm 11 --oem 3"

    ldir = os.listdir("Source/FrameFiles/")
    num_list = [int(element.strip("frame.png")) for element in ldir]
    num_list.sort()
    maximum_frame = num_list[-1]

    # start, duration, keywords

    frame_dict = []
    #cycle through all frames in the file
    for i in range(0, maximum_frame + 1, int(fps/2)):
        print(f"Processing: {i}")
        text = pytesseract.image_to_string(Image.open(f"Source/FrameFiles/frame{i}.png"), config=myconfig)
        possible_keys = []
        for word in keywords:
            key_list = word.split(" ")
            #list comp each word of key statement is in text
            element_list = [element for element in key_list if element in text]
            if len(key_list) == len(element_list):
                possible_keys.append(word)

        if len(possible_keys) != 0:
            frame_dict.append({i : possible_keys})
    
    print(frame_dict)

    #return success, transcript_dict