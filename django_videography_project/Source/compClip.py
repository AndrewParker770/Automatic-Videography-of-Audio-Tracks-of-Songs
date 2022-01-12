from moviepy.editor import *
from PIL import Image

import os
import random
import re
import numpy as np

def color_clip(size, duration, fps=25, color=(0,0,0), output='color.mp4'):
    return ColorClip(size, color, duration=duration)

def create_image_clip(file_path, img_duration):
    image_clip = ImageClip(file_path, duration=img_duration)
    image_clip.set_position(("center","center")).resize( (460,720) )
    return image_clip

def getTimings(keywords, transcript, youtubeID):
    timings = []
    for section in transcript[0][youtubeID]:
        #extract text and remove newline and punctuation
        text = section['text'].lower()
        text = re.sub('[\n]+', ' ', text)
        text = re.sub('[^a-zA-Z ]+', '', text)

        # does this section have a key word
        possible_keys = []
        for word in keywords:
            if word in text:
                possible_keys.append(word)
        
        # no keys this section?
        if len(possible_keys) == 0:
            continue
        
        #order these possible keys, based on appearance in lyrics
        possible_keys.sort(key=text.find)

        section_duration = section['duration']
        section_start = section['start']

        #calculate the times and durations each image will be shown
        DIVIDE_EQUALLY = True
        if DIVIDE_EQUALLY:
            # if assuming to when images should be displayed
            num_keys = len(possible_keys)
            
            duration_step = section_duration/num_keys
            counter = 0
            for key in possible_keys:
                time = {'key': key, 'start': section_start + (duration_step * counter), 'duration': duration_step}
                counter += 1
                timings.append(time)
        else:
            # if only using one image per section
            key = possible_keys[0]
            time = {'key': key, 'start': section_start, 'duration': section_duration}
            timings.append(time)

    return(timings)

def compileTimings(timings, song_duration, youtubeID, audio_clip):

    #create template
    size = (200, 100)
    template_clip = color_clip(size, song_duration)

    # sort timings from biggest to smallest buffer
    timings.sort(reverse=True, key= lambda el: el['start'])

    clips =[template_clip]
    for entry in timings:
        word = entry['key']
        
        #make buffer clip of appropraite length
        start_time = entry['start']
        buffer_clip = color_clip(size, start_time)


        #create random img clip from corresponding image folder
        img_duration = entry['duration']
        file_path = os.path.join(os.curdir, f'videography/static/imgs/{word}')
        img = random.choice(os.listdir(file_path))
        img_source = os.path.join(file_path, img)
        image_clip = create_image_clip(img_source, img_duration)

        #combine buffer and img clips and save in clips
        final_clip = concatenate_videoclips([buffer_clip, image_clip], method='compose')
        clips.append(final_clip)

    comp_clip = CompositeVideoClip(clips)
    comp_clip.audio = audio_clip
    comp_clip.write_videofile(f"videography/static/videos/{youtubeID}.mp4", fps=24)
