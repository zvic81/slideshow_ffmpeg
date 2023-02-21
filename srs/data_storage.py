# functions and  storage for list objects (local database)
from entities import VideoSource

# import schemas


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


def create_video_object(*, status: str, video_url: str, picture_list: list) -> VideoSource:
    video_source = VideoSource()
    # slide.pics_list =  schemas.PictureSourceSchema(many=True).load(picture_list)  ************Decomment for load from local dict
    video_source.pics_list = picture_list.copy()
    video_source.status = status
    video_source.video_url = video_url
    return video_source


#  add test object to VideoList from test_list
def append_test_video(status="NEW", video_url="/home/python/vid.mp4"):
    z = create_video_object(status=status, video_url=video_url, picture_list=test_list)
    Video_List.append(z)


# from threading import Thread
# th = Thread(target=sleepMe, args=(i, ))
# th.start()
