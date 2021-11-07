import librosa.display
import librosa
import sys
import helperFunctions
import warnings


if __name__ == "__main__":
    nameOfFile = sys.argv[1]
    #youtubeLinkID = helperFunctions.getID(youtubeLink)

    filename = 'AudioFiles/%s.wav'%(nameOfFile)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        y, sr = librosa.load(filename)

    tempo, beat_frames = librosa.beat.beat_track(y, sr)

    print('Tempo: {:.2f}'.format(tempo))

    beat_times = librosa.frames_to_time(beat_frames, sr)

    print(beat_times)

    duration = librosa.get_duration(y, sr)

    print("Duration: {:.2f}".format(duration))

    #pygame.mixer.pre_init(44100, 16, 2, 4096)
    #pygame.init()

    #infoObject = pygame.display.Info()

    #screen_w = int(infoObject.current_w/2.2)    
    #screen_h = int(infoObject.current_w/2.2)

    # Set up the drawing window
    #screen = pygame.display.set_mode([screen_w, screen_h])

    #MUSIC_END = pygame.USEREVENT+1
    #pygame.mixer.music.load(filename)
    #pygame.mixer.music.play(-1)
    #pygame.mixer.music.set_endevent(MUSIC_END)

    #clock = pygame.time.Clock()

    #running = True
    #while running:
    #    for event in pygame.event.get():
    #        if event.type == MUSIC_END:
    #            running = False
##
    #    clock.tick(60)

        
        


