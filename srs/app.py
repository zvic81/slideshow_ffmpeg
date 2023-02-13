"""
Slideshow_ffmpeg - REST API server, receiving list of json data as {pics_URL, duration, transition, caption} and building video file using ffmpeg.
Film is slideshow from pictures with effects transition (xfade)
User get video ID back and sending it to endpoints can get status video (making, ready) and the finished video (using curl)
# to download video <curl --location --request GET "http://localhost:5000/video/fdba0bcf62f14b6eb266aa03cf0b038b" --output testvideo.mpg >
"""
from apiflask import APIFlask
import logging
import schemas
from routes import configure_routes

# import ffmpeg_function dont need


app = APIFlask(__name__)
configure_routes(app)
app.url_map.strict_slashes = False  # open /index/ as /index
app.config["DESCRIPTION"] = "Slideshow - RestAPI server"
app.config["BASE_RESPONSE_SCHEMA"] = schemas.BaseResponse
# the data key should match the data field name in the base response schema
# defaults to "data"
app.config["BASE_RESPONSE_DATA_KEY "] = "data"

# logging.basicConfig(
#     level=logging.INFO,
#     handlers=[
#         logging.FileHandler("slideshow_log.log", mode="w"),
#         logging.StreamHandler(),
#     ],
#     # filename="slideshow_log.log",
#     # filemode="w",
#     format="%(asctime)s %(levelname)s %(message)s",
# )
def init_logger(name):
    logger = logging.getLogger(name)
    FORMAT = "%(asctime)s :: %(name)s :: %(lineno)s :: %(levelname)s :: %(message)s"
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(logging.Formatter(FORMAT))
    fh = logging.FileHandler(filename="slideshow_log.txt", mode="w")
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter(FORMAT))
    logger.addHandler(sh)
    logger.addHandler(fh)
    logger.info("Logger was initialitation")
    pass


if __name__ == "__main__":
    init_logger("app")
    logger = logging.getLogger("app.main")
    logger.info("app started!!!")
    app.run(debug=0, host="127.0.0.1")
    pass


"""  test data 
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
"""
