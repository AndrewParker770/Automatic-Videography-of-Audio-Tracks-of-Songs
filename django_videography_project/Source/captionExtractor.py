from Source.audioStripper import getID
import sys
from youtube_transcript_api import YouTubeTranscriptApi
from Source.extractText import returnKeyWords

def getKeywords(youtubeLinkID, caption_bool):
    stopwords = getStopWords("Source/stopwords.txt")

    if caption_bool:
        try:
            transcript = YouTubeTranscriptApi.get_transcripts([youtubeLinkID], languages=['en'])
        except:
            return False
        
        keywords = set([])
        for section in transcript[0][youtubeLinkID]:
            result = returnKeyWords(section['text'], 1)
            if result != []:
                keywords.add(result[0][0])
        return keywords

    elif not caption_bool:
        keywords = set([])
        with open(f'Source/TextFiles/{youtubeLinkID}.txt') as f:
            lines = f.readlines()
        print(lines)
        
    


def flattenTranscript(transcript):
    wholeTranscript = ''
    for line in transcript[0][youtubeLinkID]:
        wholeTranscript += (line['text'] + ' ') 
    return wholeTranscript

def getStopWords(filename):
    with open(filename) as f:
        stopwords = f.read().splitlines()
    return stopwords


if __name__ == "__main__":
    youtubeLink = sys.argv[1]
    youtubeLinkID = getID(youtubeLink)

    print(getTranscript(youtubeLinkID))