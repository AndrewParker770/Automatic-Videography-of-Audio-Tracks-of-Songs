import helperFunctions
import sys
from youtube_transcript_api import YouTubeTranscriptApi

def extractTranscript(transcript):
    wholeTranscript = ''
    for line in transcript[0][youtubeLinkID]:
        wholeTranscript += (' ' + line['text']) 
    return wholeTranscript


if __name__ == "__main__":
    youtubeLink = sys.argv[1]
    youtubeLinkID = helperFunctions.getID(youtubeLink)

    transcriptFound = False

    try:
        transcript = YouTubeTranscriptApi.get_transcripts([youtubeLinkID], languages=['en'])
        transcriptFound = True
    except:
        print("Transcript could not be found.")
        transcriptFound = False

    wholeTranscript = extractTranscript(transcript)

    print(wholeTranscript)

