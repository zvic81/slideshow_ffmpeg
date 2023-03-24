#  functions for working with library ffmpeg and creating video from pictures
# Bash command we need is
# ffmpeg -loop 1 -t 5 -i 001.png -loop 1 -t 5 -i 020.png -loop 1 -t 5 -i 050.png
# -filter_complex "[0][1]xfade=transition=fade:duration=2:offset=4[vf1]; [vf1][2]xfade=transition=fade:duration=5:offset=8" output.mp4
# ffmpeg -i logo.png -vf scale=360:640 output_1.png

import ffmpeg
from pathlib import Path
from time import sleep
from threading import Thread
import logging
import shutil  # for delete dir

import gcp_functions
from entities import VideoSource
from data_storage import Video_Dict


BASE_RESOLUTION = (1280, 720)
logger = logging.getLogger("app.main.ffmpeg")


def get_video_size(filename: str) -> tuple:
    try:
        logger.info("get_video_size for %s", filename)
        probe = ffmpeg.probe(filename)
        video_info = next(s for s in probe["streams"])
        width = int(video_info["width"])
        height = int(video_info["height"])
        return width, height
    except ffmpeg.Error as e:
        logger.error(e)
        return 1


#  download and resize picture to make the same size before starting filter ffmpeg. New picture's size is not larger one of (base_size_x,base_size_y)
def load_and_resize_picture(*, input_url: str, output_dir: str, base_size_x=1280, base_size_y=720, count_file_name: str) -> str:
    if not len(input_url) or type(input_url) != str:
        logger.error("len(input_url) and type(input_url) != str")
        return 1
    file_out = check_create_dir(output_dir) + "/" + \
        str(count_file_name) + '.png'
    try:
        pic_x, pic_y = get_video_size(input_url)
    except TypeError:
        logger.error("get_video_size returns 1 arg, must 2, wrong URL!")
        return 1

    # MAKE checking errors!!!!!!!!!!!!!!!
    scale = min(base_size_x / pic_x, base_size_y / pic_y)
    pic_x = int((scale * pic_x) + 0.5)
    pic_y = int((scale * pic_y) + 0.5)
    try:
        logger.info("load_and_resize_picture for %s", input_url)
        (
            ffmpeg.input(input_url)
            .filter("scale", pic_x, pic_y)
            .output(file_out, y="-y")
            .run()
        )
    except ffmpeg.Error as e:
        logger.error(e)
        return 1
    return file_out


# check and create dir for saving picture before resize
def check_create_dir(dir_name: str) -> str:
    import data_storage
    dir_name = str(data_storage.PICS_DIR) + '/' + dir_name
    Path(dir_name).mkdir(parents=True, exist_ok=True)
    return dir_name


#  convert list of pictures to video with xfade ffmpeg. Argument is objects of video_source. Return url video and add it to Video_Dict
def convert_pic_to_video(video_source: VideoSource) -> str:
    import data_storage
    logger.info("start ffmpeg")
    if type(video_source) != VideoSource:
        logging.error(
            "convert_pic_to_video: type(video_source) != video_source")
        return 1
    video_source.status = "IN_PROGRESS"
    Video_Dict[video_source.get_uid()] = video_source.status
    if len(video_source.pics_list) < 2:
        video_source.status = "ERROR"
        Video_Dict[video_source.get_uid()] = video_source.status
        logging.error("convert_pic_to_video: len(video_source.pics_list) < 2")
        return 1  # must be 2 or more pictures in video_source, else cant make transition
    sum_offset = 0
    previous_pic = None
    for curr_pic in video_source.pics_list:
        if previous_pic:  # pass first object in list
            file2 = load_and_resize_picture(
                input_url=curr_pic.srs, output_dir=video_source.get_uid(), count_file_name=sum_offset + 1
            )
            if file2 == 1:
                logger.error("error load_and_resize_picture(file2)")
                video_source.status = "ERROR"
                Video_Dict[video_source.get_uid()] = video_source.status
                return 1
            if not sum_offset:  # only for 2 round of cycle
                file1 = load_and_resize_picture(
                    input_url=previous_pic.srs, output_dir=video_source.get_uid(), count_file_name=sum_offset + 101
                )
                if file1 == 1:
                    logger.error("error load_and_resize_picture(file1)")
                    video_source.status = "ERROR"
                    Video_Dict[video_source.get_uid()] = video_source.status
                    return 1
                faded = ffmpeg.input(
                    file1, t=previous_pic.duration + 1, loop=1)
                # continue here
                # faded = ffmpeg.filter((faded), "scale", size="320:135")
                pad_x, pad_y = get_video_size(file1)
                pad_x = (BASE_RESOLUTION[0] - pad_x) / 2
                pad_y = (BASE_RESOLUTION[1] - pad_y) / 2
                faded = ffmpeg.filter(
                    (faded),
                    "pad",
                    str(BASE_RESOLUTION[0]),
                    str(BASE_RESOLUTION[1]),
                    str(pad_x),
                    str(pad_y),
                    "red",
                )
            stream2 = ffmpeg.input(file2, t=curr_pic.duration + 1, loop=1)
            pad_x, pad_y = get_video_size(file2)
            # enter check error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
            pad_x = (BASE_RESOLUTION[0] - pad_x) / 2
            pad_y = (BASE_RESOLUTION[1] - pad_y) / 2
            stream2 = ffmpeg.filter(
                (stream2),
                "pad",
                str(BASE_RESOLUTION[0]),
                str(BASE_RESOLUTION[1]),
                str(pad_x),
                str(pad_y),
                "red",
            )

            sum_offset += previous_pic.duration
            try:
                faded = ffmpeg.filter(
                    (faded, stream2),
                    "xfade",
                    transition=curr_pic.transition,
                    duration=1,
                    offset=sum_offset,
                )
            except ffmpeg.Error as e:
                logger.error(e)
                Video_Dict[video_source.get_uid()] = "ERROR"
                return 1
            pass
        previous_pic = curr_pic
        pass

    # file_video = PICS_DIR + "/" + "id111" + "/video_out.mpg" FOR TEST local
    file_video = str(data_storage.PICS_DIR) + '/' + \
        video_source.get_uid() + "/video_out.mpg"
    try:
        logger.info("start making fade id = %s", video_source.get_uid())
        out = (
            ffmpeg.output(faded, file_video, y="-y")
            .global_args("-loglevel", "error")
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as exc:
        logger.error("Error in making fade %s", video_source.get_uid())
        logger.error(exc.stderr.decode("utf8"))
        logger.error(exc.stdout.decode("utf8"))
        video_source.status = "ERROR"
        Video_Dict[video_source.get_uid()] = video_source.status
        return 1
    video_source.video_url = file_video
    if move_video_to_firebase(video_source.get_uid()):
        logger.error("Error in moving video %s", video_source.get_uid())
        return 1
    logger.info("Success moving to firebase video id = %s",
                video_source.get_uid())
    video_source.status = "READY"
    Video_Dict[video_source.get_uid()] = video_source.status
    logger.info("Success making video id = %s", video_source.get_uid())
    return 0


# move video from dir to firebase (with deleting original dir)
def move_video_to_firebase(video_id: str):
    import data_storage

    video_url = Path(str(data_storage.PICS_DIR) +
                     '/' + video_id + "/video_out.mpg")
    # Path(str(data_storage.PICS_DIR) + video_id + "/video_out.mpg")
    if not video_url.is_file():
        logger.error(
            "Error in move_video_to_firebase, no video_out.mpg in dir %s", video_id)
        return 1
    gcp_functions.upload_blob(video_url, video_id + '.mpg')
    logger.info('video %s upload to firebase', video_id + '.mpg')
    try:
        shutil.rmtree(Path(str(data_storage.PICS_DIR) + '/' + video_id))
        logger.info('dir removed %s', video_id)
    except OSError as e:
        logger.error(
            "Error in move_video_to_firebase, cant del dir %s", video_id)
        return 1
    return 0


if __name__ == "__main__":
    # move_video_to_firebase('')

    pass


# (
#     ffmpeg.input("pics/logo.png")
#     .filter("scale", 360, 640)
#     .output("pics/output_1.png", y="-y")
#     .run()
# )
# stream = ffmpeg.input("pics/output_1.png", t=5, loop=1)
# stream2 = ffmpeg.input("pics/050.png", t=5, loop=1)
# faded = ffmpeg.filter(
#     (stream, stream2), "xfade", transition="fade", duration=3, offset=2
# )
# stream2 = ffmpeg.input("pics/020.png", t=5, loop=1)
# faded = ffmpeg.filter(
#     (faded, stream2), "xfade", transition="fade", duration=5, offset=4
# )
# out = ffmpeg.output(faded, "pics/out444.mpg", y="-y")
# ffmpeg.run(out)
