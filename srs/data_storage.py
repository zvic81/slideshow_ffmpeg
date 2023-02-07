# functions and  storage for list objects (local database)
from entities import Slide, PictureSource
import schemas


Video_List = []  # General list contains objects of Slide

test_list = [
    {
        "srs": "pics.com\\11/001.png",
        "duration": 2,
        "transition": "fade",
        "caption": "Lalala",
    },
    {
        "srs": "pi.ru\\22/020.png",
        "duration": 2,
        "transition": "fade",
        "caption": "fade2",
    },
    {
        "srs": "pi.ru\\33/050.png",
        "duration": 2,
        "transition": "fade",
        "caption": "fade3",
    },
]


def create_slide(*, status: str, video_url: str, picture_list: list) -> Slide:
    slide = Slide()
    # slide.pics_list =  schemas.PictureSourceSchema(many=True).load(picture_list)  ************Decomment for load from local dict
    slide.pics_list = picture_list.copy()
    slide.status = status
    slide.video_url = video_url
    return slide


#  add test object to VideoList from test_list
def append_test_video(status="NEW", video_url="/home/python/vid.mp4"):
    z = create_slide(status=status, video_url=video_url, picture_list=test_list)
    Video_List.append(z)


# from threading import Thread
# th = Thread(target=sleepMe, args=(i, ))
# th.start()
