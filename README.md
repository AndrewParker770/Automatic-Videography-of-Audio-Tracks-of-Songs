# Automatic-Videography-of-Audio-Tracks-of-Songs

This following repository contains a prototype automatic videography generation system. More specifically, given any YouTube video of a song, the system automatically retrieves a set of images that are related to each line of the song, and inserts these images in an automatically created video track seeking to align these images with the background audio. 

### Prerequisite
This system was created and tested using a Windows Operating system, and although the system should permit the use of other operating systems 

* [Python v3.8.12](https://www.python.org/)
    * Use python version equivalent to, or greater than, verison 3.8.12.
    * Python version can be found using the ``` python --version ``` command.
* [Google Tesseract OCR](https://tesseract-ocr.github.io/tessdoc/Home.html)
    * [Windows Installer](https://github.com/UB-Mannheim/tesseract/wiki)
        * Install either the 32 bit or 64 bit installer depending on your system specifications.
        * Allow installer to run using the deafult values, and add the install location to your path, for example: ```C:\Program Files\Tesseract-OCR ```
        * Create an evironment variable called "TESSDATA_PREFIX" which contains the path to the "tessdata" folder in the "Tesseract-OCR" program folder, for example: ```C:\Program Files\Tesseract-OCR\tessdata```
    * [Generic Install Page](https://tesseract-ocr.github.io/tessdoc/Home.html)
        * Follow install instructions in the link above for your operating system.
        * Add the install location to your path.
        * Create an evironment variable called "TESSDATA_PREFIX" which contains the path to the "tessdata" folder in the "Tesseract-OCR" program folder.

* [Chrome](https://support.google.com/chrome/answer/95346?hl=en-GB&co=GENIE.Platform%3DDesktop)
    * Must be the most up to date version avalable.
        1. To check, open chrome and open "More", which appears as three vertical dots on the top right of the window.
        2. Then go to "Help", open "About Google Chrome".
        3. Under "About Chrome", check if there is an update available and download it if so.

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
. venv/Scripts/activate
```
```bash
python -m pip install --upgrade pip
```
```bash
pip install Pillow
```
```bash
pip install -r requirements.txt
```
```bash
python -m pip install --upgrade pytube
```
```bash
pip install git+https://github.com/ssuwani/pytube
```
```bash
python -m pip install --upgrade pytube
```
```bash
cd django_videography_project
```
```bash
python manage.py runserver
```
Terminal output should prompt to open browser and access [local host.](http://127.0.0.1:8000/)


### Collections
The system may store videos internally during the video generation process, however these videos (as well as any file made during its creation) are deleted once another video is generated. This is in part to prevent excessive files being stored, however this is mainly due to the issue of storing vidoes which are based on copyrighted content such as much music is.

However, a collection folder for demonstration purposes have been provided in the system and if required you can manually enable saving videos to the collection by creating an evironment variable before starting the django server as follows:
```bash export COLLECT_JSON=True ```

### Example of video generation
By supplying the forced alignment method in the prototypes menu and inputting the 
* youtube url: https://www.youtube.com/watch?v=1iiDp6ga_qQ
* artist name: America
* song name: A Horse With No Name

We can take the video (found at https://www.youtube.com/watch?v=1iiDp6ga_qQ) which appears as a lyrics video as follows:

![Horse](https://user-images.githubusercontent.com/60265517/154803583-861308dd-34c4-4c5d-92e0-bccca53493e6.PNG)

This video is then converted into the following:

https://user-images.githubusercontent.com/60265517/154802216-56c4354d-1dae-4fb6-ab60-3cf1260c77b8.mp4

The figure below shows a section of the entries in timing dictionary which created each image, in the video above, shown in a timeline:

![Timings](https://user-images.githubusercontent.com/60265517/154803847-f448016f-33b3-474a-b07c-99e7c93bc10c.PNG)

### Citations

[C. Gupta, E. Yılmaz and H. Li, "Automatic Lyrics Alignment and Transcription in Polyphonic Music: Does Background Music Help?," ICASSP 2020 - 2020 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Barcelona, Spain, 2020, pp. 496-500, doi: 10.1109/ICASSP40776.2020.9054567.](https://ieeexplore.ieee.org/document/9054567)

#### Project Information

This prototype was created as part of a Level 4 project at the University of Glasgow.

Created by: Andrew Parker & Debasis Ganguly
