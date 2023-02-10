#  routes for rest api server's endpoints


from flask import redirect, send_from_directory
from werkzeug.exceptions import NotFound
import os
from threading import Thread
import logging
import schemas
from data_storage import append_test_video, Video_List, create_slide
from ffmpeg_function import convert_pic_to_video


def configure_routes(app):
    logger = logging.getLogger("app.main.routes")

    @app.get("/")
    @app.doc(hide=True)
    def index():
        data = {"message": "Hello!"}
        # open swagger index page
        logger.info("server made redirect")
        return redirect("http://localhost:5000/docs", code=302)

    @app.get("/video")
    @app.output(schemas.VideoOutSchema(many=True), status_code=200)
    def get_list_videos():
        if not len(Video_List):  # only for TEST, fill list test data if it empty
            append_test_video()
            append_test_video(status="NEW", video_url="tetetet\tete\te")
        return {
            "data": Video_List,
            "code": 200,
        }

    @app.post("/video")
    @app.input(schemas.PictureSourceSchema(many=True))
    @app.output(schemas.VideoId, status_code=201)
    def post_picture_list(data):
        if len(data) < 2:
            logger.error("Number of images less 2 ")
            return {
                "data": {"id": "Number of images less 2"},
                "code": 400,
            }, 400
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

    @app.get("/status/<string:video_id>")
    @app.output(schemas.VideoStatus, status_code=200)
    def get_status_video(video_id):
        response = "ID not exists"
        code = 404
        for slide in Video_List:
            if video_id == slide.get_uid():
                code = 200
                response = slide.status
        return {
            "data": {"status": response},
            "code": code,
        }

    @app.get("/video/<string:video_id>")
    def get_video_from_id(video_id):
        video_url = None
        for slide in Video_List:
            if video_id == slide.get_uid():
                video_url = slide.video_url if slide.status == "READY" else "NotReady"
        if video_url is None:
            logger.error("ID not exists id = %s", video_id)
            return {"data": "ID not exists", "code": 404}, 404
        if video_url == "NotReady":
            logger.error("Video not ready id = %s", video_id)
            return {"data": "Video not ready, wait or recreate", "code": 404}, 404
        app_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )  # path to video in list objects is "pics/id111/video_out.mpg"
        try:
            logger.info("try to give out video id = %s", video_id)
            return send_from_directory(app_dir, video_url, as_attachment=False)
        except NotFound:
            logger.error("File video not found id = %s", video_id)
            return {
                "data": "File video not found, recreate it",
                "code": 404,
            }, 404
