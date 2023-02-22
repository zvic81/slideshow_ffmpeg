# functions and  storage for list objects (local database)
from entities import VideoSource
PICS_DIR = "/pics/"

Video_Dict = {}  # General dict contains records like {id_video: status_video}

test_list = [
    {
        "caption": "SuperShow",
        "duration": 3,
        "srs": "https://webmg.ru/wp-content/uploads/2022/10/i-17-15.jpeg",
        "transition": "fade"
    },
    {
        "caption": "SuperShow",
        "duration": 2,
        "srs": "https://i.pinimg.com/originals/f3/e9/ee/f3e9eeddfe1cc62853167b7183cc324a.png",
        "transition": "fade"
    },
    {
        "caption": "SuperShow",
        "duration": 4,
        "srs": "https://i.ytimg.com/vi/ULEprOna8-g/maxresdefault.jpg",
        "transition": "fade"
    }
]


def create_video_object(*, status: str, video_url: str, picture_list: list) -> VideoSource:
    video_source = VideoSource()
    # slide.pics_list =  schemas.PictureSourceSchema(many=True).load(picture_list)  ************Decomment for load from local dict
    video_source.pics_list = picture_list.copy()
    video_source.status = status
    video_source.video_url = video_url
    return video_source


#  add test object to VideoList from test_list
def append_test_video(status="NEW", video_url="/home/python/vid.mp4"):
    # z = create_video_object(
    #     status=status, video_url=video_url, picture_list=test_list)
    # Video_List.append(z)
    pass


# from threading import Thread
# th = Thread(target=sleepMe, args=(i, ))
# th.start()
