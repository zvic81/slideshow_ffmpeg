"""
Slideshow_ffmpeg - REST API server, receiving list of json data as {pics_URL, duration, transition, caption} and building video file using ffmpeg.
Film is slideshow from pictures with effects transition (xfade)
User get video ID back and sending it to endpoints can get status video (making, ready) and the finished video (using curl)
"""
from apiflask import APIFlask

import schemas
from routes import configure_routes


app = APIFlask(__name__)
configure_routes(app)
app.url_map.strict_slashes = False  # open /index/ as /index
app.config["DESCRIPTION"] = "Slideshow - RestAPI server"
app.config["BASE_RESPONSE_SCHEMA"] = schemas.BaseResponse
# the data key should match the data field name in the base response schema
# defaults to "data"
app.config["BASE_RESPONSE_DATA_KEY "] = "data"


if __name__ == "__main__":

    app.run(debug=0, host="127.0.0.1")
    pass


"""  test data 
[
  {
    "caption": "SuperShow",
    "duration": 15,
    "srs": "pics.com\\11/001.png",
    "transition": "fade"
  },
  {
    "caption": "SuperShow",
    "duration": 20,
    "srs": "pics.com\\11/020.png",
    "transition": "fade"
  },  
 {
    "caption": "SuperShow",
    "duration": 10,
    "srs": "pics.com\\11/050.png",
    "transition": "fade"
  }
]
"""
