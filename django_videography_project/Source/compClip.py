from moviepy.editor import *
from PIL import Image

import os
import random
import re
import numpy as np
import shutil


def color_clip(size, duration, fps=25, color=(0,0,0), output='color.mp4'):
    return ColorClip(size, color, duration=duration)

def create_image_clip(file_path, img_duration):
    image_clip = ImageClip(file_path, duration=img_duration)
    image_clip.set_position(("center","center")).resize( (460,720) )
    return image_clip

def getTimings(keywords, transcript):
    timings = []
    for section in transcript:
        #extract text and remove newline and punctuation
        text = section['text'].lower()
        text = re.sub('[\n]+', ' ', text)
        text = re.sub('[^a-zA-Z ]+', '', text)

        # does this section have a key word
        possible_keys = []
        for word in keywords:
            key_list = word.split(" ")
            #list comp each word of key statement is in text
            element_list = [element for element in key_list if element in text]
            if len(key_list) == len(element_list):
                possible_keys.append(word)
        
        # no keys this section?
        if len(possible_keys) == 0:
            continue
        
        #order these possible keys, based on appearance in lyrics
        possible_keys.sort(key=lambda element: text.find(element.split(" ")[0]))

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

def compileTimings(timings, song_duration, youtubeID, audio_clip, COLLECT_JSON):

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

        #make a single word 
        words = word.split(" ")
        filename = "-".join(words)

        #create random img clip from corresponding image folder
        img_duration = entry['duration']
        file_path = os.path.join(os.curdir, f'videography/static/imgs/{filename}')
        img = random.choice(os.listdir(file_path))
        img_source = os.path.join(file_path, img)
        image_clip = create_image_clip(img_source, img_duration)

        #combine buffer and img clips and save in clips
        final_clip = concatenate_videoclips([buffer_clip, image_clip], method='compose')
        clips.append(final_clip)

    comp_clip = CompositeVideoClip(clips)
    comp_clip.audio = audio_clip
    comp_clip.write_videofile(f"videography/static/videos/{youtubeID}.mp4", fps=24)

    if COLLECT_JSON:
        shutil.move(f"videography/static/videos/{youtubeID}.mp4", f"videography/static/collection/{youtubeID}.mp4")

def findConflicts(timings):
    timings.sort(key=lambda n: n["start"])
    conflict_found = False
    new_timing_list = []
    for counter, timing in enumerate(timings):
        if counter+1 == len(timings):
            break
        timing_start = timings[counter]["start"]
        timing_end = timings[counter]["start"] + timings[counter]["duration"]

        new_timing = None
        next_timing_start = timings[counter+1]["start"]
        if next_timing_start < timing_end:
            conflict_found = True
            new_timing = timing
            new_timing['duration'] = next_timing_start - timing_start
        
        if new_timing == None:
            new_timing = timing
        
        new_timing_list.append(new_timing)
        new_timing_list.sort(key=lambda n: n["start"], reverse=True)
    
    return conflict_found, new_timing_list

def getLyricTimings(frame_list, fps):
    previous_timing = []
    timings = []
    key_word_list = None
    for entry_dict in frame_list:
        key, value = list(entry_dict.items())[0]
        if len(previous_timing) == 0:
            # just starting the streth of frames
            previous_timing.append(key)
            key_word_list = value
        elif value == key_word_list:
            # another frame in a strech, add frame number and continue
            previous_timing.append(key)
        elif value != key_word_list:

            #determine total duration
            start_time = (previous_timing[0]/(fps/2)) * 0.5
            end_time = (previous_timing[-1]/(fps/2)) * 0.5
            duration = end_time - start_time

            # determine timings
            duration_step = duration / len(value)
            counter = 0
            for word in key_word_list:
                time = {'key': word, 'start': start_time + (duration_step * counter), 'duration': duration_step}
                counter += 1
                timings.append(time)

            # reset previous timings and add new frame and key_word list 
            previous_timing = [key]
            key_word_list = value

    #deal with remaing timings
    #determine total duration
    start_time = (previous_timing[0]/(fps/2)) * 0.5
    end_time = (previous_timing[-1]/(fps/2)) *0.5
    duration = end_time - start_time

    # determine timings
    duration_step = duration / len(value)
    counter = 0
    for word in key_word_list:
        time = {'key': word, 'start': start_time + (duration_step * counter), 'duration': duration_step}
        counter += 1
        timings.append(time)

    
    conflict_found, new_timing_list = findConflicts(timings)
    
    return new_timing_list