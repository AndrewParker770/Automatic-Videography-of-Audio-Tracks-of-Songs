from Source.audioStripper import getID
import sys
from youtube_transcript_api import YouTubeTranscriptApi
from Source.extractText import returnKeyWords
import os

"""
def getKeywords(youtubeLinkID, caption_bool):
    stopwords = getStopWords("Source/stopwords.txt")

    transcript = getTranscript(youtubeLinkID)
        
    keywords = set([])
    for section in transcript[0][youtubeLinkID]:
        result = returnKeyWords(section['text'], 1)
        if result != []:
            keywords.add(result[0][0])
    return keywords
"""


def getCaptions(youtubeID):
    transcript_dict = YouTubeTranscriptApi.get_transcripts([youtubeID], languages=['en'])
    with open(f"Source/TextFiles/{youtubeID}.txt", "w") as f:
        for line in transcript_dict[0][youtubeID]:
            text = line['text']
            if text[-1] != '\n':
                text += '\n'
            f.write(text)
    return os.path.exists(f"Source/TextFiles/{youtubeID}.txt"), transcript_dict
        
    
def flattenTranscript(transcript):
    wholeTranscript = ''
    for line in transcript[0][youtubeLinkID]:
        wholeTranscript += (line['text'] + ' ') 
    return wholeTranscript

def getStopWords(filename):
    with open(filename) as f:
        stopwords = f.read().splitlines()
    return stopwords
