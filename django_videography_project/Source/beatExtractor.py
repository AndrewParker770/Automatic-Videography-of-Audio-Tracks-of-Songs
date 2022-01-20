import librosa.display
import librosa
import sys
import warnings


if __name__ == "__main__":
    nameOfFile = sys.argv[1]

    filename = 'AudioFiles/%s.wav'%(nameOfFile)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        y, sr = librosa.load(filename)

    tempo, beat_frames = librosa.beat.beat_track(y, sr)

    print('Tempo: {:.2f}'.format(tempo))

    beat_times = librosa.frames_to_time(beat_frames, sr)

    print(beat_times)