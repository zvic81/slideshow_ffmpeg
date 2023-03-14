#  routes for rest api server's endpoints


from flask import redirect, send_from_directory
from werkzeug.exceptions import NotFound
import os
from pathlib import Path
from threading import Thread
import logging
import shutil
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
        return redirect("http://localhost:5000/docs", code=302)

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
            logger.error("Video not ready, id = %s", video_id)
            return {
                "data": status,
                "code": 404,
            }, 404
        # del and create dir PICS
        shutil.rmtree(Path(str(data_storage.PICS_DIR)))
        Path(str(data_storage.PICS_DIR)).mkdir(parents=True, exist_ok=True)

        video_url = Path(str(data_storage.PICS_DIR) + '/' + video_id + '.mpg')
        gcp_functions.download_blob(
            video_id + '.mpg', video_url)
        if not video_url.is_file():
            logger.error("Video not found, id = %s", video_id)
            return {
                "data": "VIDEO_NOT_FOUND",
                "code": 404,
            }, 404
        try:
            logger.info("try to give out video id = %s", video_id)
            return send_from_directory(data_storage.PICS_DIR, video_id + '.mpg', as_attachment=False)
        except NotFound:
            logger.error("File video not found id = %s", video_id)
        return {
            "data": 'ERROR_SEND_FILE',
            "code": 404,
        }, 404
        pass
