#  routes for rest api server's endpoints
from flask import redirect, abort
from threading import Thread
import schemas
import entities
from data_storage import append_test_video, Video_List, create_slide
from ffmpeg_function import convert_pic_to_video


def configure_routes(app):
    @app.get("/")
    @app.doc(hide=True)
    def index():
        data = {"message": "Hello!"}
        # open swagger index page
        return redirect("http://localhost:5000/docs", code=302)

    @app.get("/video")
    @app.output(schemas.VideoOutSchema(many=True), status_code=200)
    def get_list_videos():
        if not len(Video_List):  # only for TEST, fill list test data if it empty
            append_test_video()
            append_test_video(status="old", video_url="tetetet\tete\te")
        return {
            "data": Video_List,
            "code": 200,
        }

    @app.post("/video")
    @app.input(schemas.PictureSourceSchema(many=True))
    @app.output(schemas.VideoId, status_code=201)
    def post_picture_list(data):
        new_slide = create_slide(status="NEW", video_url="None", picture_list=data)
        Video_List.append(new_slide)
        response = new_slide.get_uid()
        # convert_pic_to_video(new_slide)
        th = Thread(target=convert_pic_to_video, args=(new_slide,))
        th.start()
        return {
            "data": {"id": response},
            "code": 201,
        }

    @app.get("/status/<string:video_id>")  #    @app.get('/goods/<int:good_id>')
    @app.output(schemas.VideoStatus, status_code=200)
    def get_status_video(video_id):
        response = "No video with this ID"
        for slide in Video_List:
            if video_id == slide.get_uid():
                response = slide.status
        return {
            "data": {"status": response},
            "code": 200,
        }
