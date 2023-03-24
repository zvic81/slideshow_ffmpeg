# functions and  storage for list objects (local database)
from entities import VideoSource
PICS_DIR = "/pics/"

Video_Dict = {}  # General dict contains records like {id_video: status_video}


def create_video_object(*, status: str, video_url: str, picture_list: list) -> VideoSource:
    video_source = VideoSource()
    # slide.pics_list =  schemas.PictureSourceSchema(many=True).load(picture_list)  ************Decomment for load from local dict
    video_source.pics_list = picture_list.copy()
    video_source.status = status
    video_source.video_url = video_url
    return video_source
