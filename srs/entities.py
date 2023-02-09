#  Store defenitions of classes
import uuid


class Slide:
    def __init__(self):
        self.pics_list = []
        self._uid = uuid.uuid4().hex  # unique ID of object slideshow
        self.video_url = ""  # url to file made video
        self.status = "EMPTY"

    def __str__(self):
        return f"*{self._uid}\n*{self.video_url}\n*{self.status}\n*{[print(i) for i in self.pics_list]}*\n\n"

    def get_uid(self):
        return self._uid


# for sourse one picture. Attributes (src, "duration", "transition", "caption")
class PictureSource:
    def __init__(self, srs: str, duration: int, transition: str, caption: str) -> None:
        self.srs = srs
        self.duration = duration
        self.transition = transition
        self.caption = caption

    def __str__(self) -> str:
        return f"\n*{self.srs}, * {self.duration}, *  {self.transition}, * {self.caption}*\n\n"
