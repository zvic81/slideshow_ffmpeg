


# Slideshow_ffmpeg
Slideshow_ffmpeg is a Python application, rest api server, which recieve list of url to picture and return ID new video. Video is slideshow sourced these pictures. Video can be downloaded whit get request (curl or browser)
User get video ID back and sending it to endpoints can get status video (making, ready) and the finished video (using curl)
For download video <curl --location --request GET "http://localhost:5000/video/fdba0bcf62f14b6eb266aa03cf0b038b" --output testvideo.mpg >
On default pics and video put in /pics/<video_id> where video_id is id each video

Endpoints:
    - Get("/video") - read all video is short format    
    - Post("/video") - create video, need list of picture, format is bellow
    - Get("/status/video_id") - read status video (in progress, ready, error). Need video_id
    - Get("/video/video_id") - get file video, need video id, use curl or browser



## Requirements

- Python 3.7+
- Flask  
- apiflask 
- venv
- ffmpeg
- threading 

## Installation

For Linux :
- 1) Clone the repository from GitHub. Then install all the dependencies.
```bash
$ git clone https://github.com/zvic81/slideshow_ffmpeg.git
```
- 2) Run python3 app.py 
```
- 3) Try open http://127.0.0.1:5000 for swagger gui app or use Postman

## Format

Example picture list:
[
  {
    "caption": "SuperShow",
    "duration": 3,
    "srs": "pics.com\\11/001.png",
    "transition": "fade"
  },
  {
    "caption": "SuperShow",
    "duration": 2,
    "srs": "pics.com\\11/020.png",
    "transition": "fade"
  },  
 {
    "caption": "SuperShow",
    "duration": 4,
    "srs": "pics.com\\11/050.png",
    "transition": "fade"
  }
]

Allowed duration from 1 to 59 (duration every clip from picture, time transition always 1 sec) 

Caption is not used in creating video

Allowed effects for transition
"fade", "wipeleft",    "wiperight",    "wipeup",    "wipedown",    "slideleft",    "slideright",    "slideup",    "slidedown",    "circlecrop",    "rectcrop",    "distance",
    "fadeblack",   "fadewhite",    "radial",    "smoothleft",    "smoothright",    "smoothup",    "smoothdown",    "circleopen",    "circleclose",    "vertopen",    "vertclose",
    "horzopen",    "horzclose",    "dissolve",    "pixelize",    "diagtl",    "diagtr",    "diagbl",    "diagbr",    "hlslice",    "hrslice",    "vuslice",    "vdslice",    "hblur",    "fadegrays",    "wipetl",    "wipetr",    "wipebl",    "wipebr",    "squeezeh",    "squeezev",    "zoomin",    "fadefast",    "fadeslow"


