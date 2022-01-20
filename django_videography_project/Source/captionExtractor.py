import sys
from youtube_transcript_api import YouTubeTranscriptApi
import os
import yake
import re



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