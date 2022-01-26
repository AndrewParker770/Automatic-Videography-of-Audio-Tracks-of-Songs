# Automatic-Videography-of-Audio-Tracks-of-Songs

This project is meant to showcase the current bounds of Information Retrieval(IR), natural language processing and tools in forced alignment

### Prerequisite

* [Python v3.x](https://www.python.org/)
* [PyTesseract](https://github.com/tesseract-ocr/tesseract#installing-tesseract)
    * Add
    * Add 
* [Chrome](https://support.google.com/chrome/answer/95346?hl=en-GB&co=GENIE.Platform%3DDesktop)
* [FFmpeg](https://www.ffmpeg.org/)
    * Should be able to run on command line within virtual environment outlined below

### Installation and Running

Open bash terminal and navigate to workspace folder. 

```bash
cd ~/<path>
```
```bash
git clone https://github.com/AndrewParker770/Automatic-Videography-of-Audio-Tracks-of-Songs.git
```

Create python virtual environment, activate it, and download the modules used by the project:

```bash
python -m venv venv
```
```bash
. venv/Script/activate
```
```bash
pip install -r requirements.txt
```

```bash
cd django_videography_project

python manage.py runserver

```
Terminal output should prompt to open browser and access [local host.](http://127.0.0.1:8000/)


### Collections

The system may store videos internally during the video generation process, however these videos (as well as any file made during its creation) are deleted once another video is generated. This is in part to prevent excessive files being stored, however this is mainly due to the issue of storing vidoes which are based on copyrighted content such as much music is.

However, collections for demonstartion purposes 

[COllections can be made this way]

If a collection has been provided

### Citations

[C. Gupta, E. Yılmaz and H. Li, "Automatic Lyrics Alignment and Transcription in Polyphonic Music: Does Background Music Help?," ICASSP 2020 - 2020 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Barcelona, Spain, 2020, pp. 496-500, doi: 10.1109/ICASSP40776.2020.9054567.](https://ieeexplore.ieee.org/document/9054567)

___

#### About me

Name: Andrew Parker

E-mail: 2389622p@student.gla.ac.uk

4th Year Computer Science Student at The University of Glasgow