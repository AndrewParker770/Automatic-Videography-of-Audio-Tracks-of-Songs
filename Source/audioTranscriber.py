import sys
import speech_recognition
import os
import helperFunctions
import audioStripper
from pydub import AudioSegment

def performTranscription(audioFileName):

    # transcribe audio file                                                         
    AUDIO_FILE = "AudioFiles/{fname}.wav".format(fname=audioFileName)

    # use the audio file as the audio source                                        
    r = speech_recognition.Recognizer()
    with speech_recognition.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file                 
        
        return("Transcription: " + r.recognize_google(audio))
    
if __name__ == "__main__":
    fileName = sys.argv[1]
    print(performTranscription(fileName))


