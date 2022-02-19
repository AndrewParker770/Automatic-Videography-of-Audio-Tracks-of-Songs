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
        spilt_line = line.lower().split(" ")
        results = returnKeyWords(line, 2)
        if results != []:
            for entry in results:
                word = entry[0]
                word_list = word.lower().split(" ")

                contains_list = []
                for elem in word_list:
                    contains_list.append(elem in spilt_line)
                
                if contains_list == [True, False]:
                    i = spilt_line.index(word_list[0])
                    word = " ".join([spilt_line[i], spilt_line[i+1]])
                elif contains_list == [False, True]:
                    i = spilt_line.index(word_list[1])
                    word = " ".join([spilt_line[i-1], spilt_line[i]])
                    
                word = word.strip('!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~')
                keywords.add(word.lower())

    return keywords

def getManual(youtubeID):
    transcript_list = YouTubeTranscriptApi.list_transcripts(youtubeID)
    try:
        transcript = transcript_list.find_manually_created_transcript(['en'])
        timing_list = transcript.fetch()
        return timing_list
    except:
        return None 

def getGenerated(youtubeID):
    transcript_list = YouTubeTranscriptApi.list_transcripts(youtubeID)
    try:
        transcript = transcript_list.find_generated_transcript(['en'])
        timing_list = transcript.fetch()

        timing_list.sort(key=lambda n: n['start'])
            
        dict_length = len(timing_list)
        for i in range(dict_length):
            if i != (dict_length - 1):
                if timing_list[i]['start'] + timing_list[i]['duration'] > timing_list[i+1]['start']:
                    timing_list[i]['duartion'] = timing_list[i+1]['start'] - timing_list[i]['start']
        return timing_list
    except:
        return None


def getCaptions(youtubeID, fakeYoutubeID):

    #check the different methods of retrieval
    transcript_dict = getManual(youtubeID)
    if transcript_dict == None:
        transcript_dict = getGenerated(youtubeID)

    #if None then retrival of captions has failed 
    if transcript_dict == None:
        return False, []
    

    with open(f"Source/TextFiles/{fakeYoutubeID}.txt", "w") as f:
        for line in transcript_dict:
            raw_line = line['text']
            #remove non_ASCII chars
            encoded_text = raw_line.encode("ascii", "ignore")
            text = encoded_text.decode()
            #remove newline chars and re-add
            text = text.replace("\n", " ")
            if text[-1] != '\n':
                text += '\n'
            f.write(text)
    return os.path.exists(f"Source/TextFiles/{fakeYoutubeID}.txt"), transcript_dict
        
    
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
    num_list =[]
    for element in ldir:
        temp_value = element.strip("frame.pngitigno") 
        if temp_value != '':
            num_list.append(int(temp_value))
    num_list.sort()
    maximum_frame = num_list[-1]

    # start, duration, keywords

    frame_list = []
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

        if len(possible_keys) == 1:
            frame_list.append({i : possible_keys})
        elif len(possible_keys) > 1:
            possible_keys.sort(key=lambda x: text.find(x))
            frame_list.append({i : possible_keys})

    return frame_list