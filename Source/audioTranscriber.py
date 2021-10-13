import sys
import speech_recognition
import os
from pydub import AudioSegment

def performTranscription(audioFileName):
    #sound = AudioSegment.from_mp3("Rjw8xiBEZfQ.mp3")
    #sound.export("Rjw8xiBEZfQ.wav", format="wav")


    # transcribe audio file                                                         
    AUDIO_FILE = "Rjw8xiBEZfQ.wav"

    # use the audio file as the audio source                                        
    r = speech_recognition.Recognizer()
    with speech_recognition.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file                  

        print("Transcription: " + r.recognize_google(audio))
    

if __name__ == "__main__":
    videoPath = sys.argv[1]

    print(performTranscription(videoPath))


