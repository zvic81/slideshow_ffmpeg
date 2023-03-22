#  routes for rest api server's endpoints


from flask import redirect
from werkzeug.exceptions import NotFound
# import os
from pathlib import Path
from threading import Thread
import logging
# import shutil
import schemas
from data_storage import Video_Dict, create_video_object
import gcp_functions


def configure_routes(app):
    logger = logging.getLogger("app.main.routes")
    from ffmpeg_function import convert_pic_to_video

    @app.get("/")
    @app.doc(hide=True)
    def index():
        data = {"message": "Hello!"}
        # open swagger index page
        logger.info("server made redirect")
        return redirect("/docs", code=302)

    @app.get("/video")  # NOT WORK!!! peharps need be deleted
    @app.output(schemas.VideoOutSchema(many=False), status_code=200)
    def get_list_videos():
        print(Video_Dict)
        # if not len(Video_List):  # only for TEST, fill list test data if it empty
        #     append_test_video()
        #     append_test_video(status="NEW", video_url="tetetet\tete\te")
        return {
            "data": "test",
            "code": 200,
        }

    @app.post("/video")  # work
    @app.input(schemas.PictureSourceSchema(many=True))
    @app.output(schemas.VideoId, status_code=201)
    def post_picture_list(data):
        if len(data) < 2:
            logger.error("Number of images less 2 ")
            return {
                "data": {"id": "WRONG_LENGTH"},
                "code": 400,
            }, 400
        new_video = create_video_object(
            status="NEW", video_url="None", picture_list=data)
        response = new_video.get_uid()
        th = Thread(target=convert_pic_to_video, args=(new_video,))
        th.start()
        return {
            "data": {"id": response},
            "code": 201,
        }

    @app.get("/status/<string:video_id>")  # work
    @app.output(schemas.VideoStatus, status_code=200)
    def get_status_video(video_id):
        response = Video_Dict.get(video_id, 'UNKNOWN')
        code = 200 if response != 'UNKNOWN' else 404
        logger.info("Video status send, id = %s, status=%s",
                    video_id, response)
        return {
            "data": {"status": response},
            "code": code,
        }

    @app.get("/video/<string:video_id>")  # not work
    def get_video_from_id(video_id):
        import data_storage
        status = Video_Dict.get(video_id, 'UNKNOWN')
        if status != 'READY':
            logger.error("Video not ready or found, id = %s", video_id)
            return {
                "data": status,
                "code": 404,
            }, 404
        video_url = gcp_functions.generate_signed_url(video_id + '.mpg')
        try:
            logger.info("try to give out video id = %s", video_id)
            return redirect(video_url, code=302)
        except NotFound:
            logger.error("URL video not found id = %s", video_id)
        return {
            "data": 'ERROR_SEND_URL',
            "code": 404,
        }, 404
        pass
