import helperFunctions
import sys
from youtube_transcript_api import YouTubeTranscriptApi
import audioTranscriber

def extractTranscript(transcript):
    wholeTranscript = ''
    for line in transcript[0][youtubeLinkID]:
        wholeTranscript += (' ' + line['text']) 
    return wholeTranscript


if __name__ == "__main__":
    youtubeLink = sys.argv[1]
    youtubeLinkID = helperFunctions.getID(youtubeLink)
    try:
        transcript = YouTubeTranscriptApi.get_transcripts([youtubeLinkID], languages=['en'])
        transcriptFound = True
    except:
        transcriptFound = False

    if (transcriptFound):
        print(transcript)
        wholeTranscript = extractTranscript(transcript)
        print(wholeTranscript)
    else:
    #    wholeTranscript = audioTranscriber.performTranscription('AudioFiles/%s'%(youtubeLinkID))
        print("Caption could not be extracted")