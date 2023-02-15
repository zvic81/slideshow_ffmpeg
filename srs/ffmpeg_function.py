#  functions for working with library ffmpeg and creating video from pictures
# Bash command we need is
# ffmpeg -loop 1 -t 5 -i 001.png -loop 1 -t 5 -i 020.png -loop 1 -t 5 -i 050.png
# -filter_complex "[0][1]xfade=transition=fade:duration=2:offset=4[vf1]; [vf1][2]xfade=transition=fade:duration=5:offset=8" output.mp4
# ffmpeg -i logo.png -vf scale=360:640 output_1.png

# https://webmg.ru/wp-content/uploads/2022/10/i-17-15.jpeg
# https://i.pinimg.com/originals/f3/e9/ee/f3e9eeddfe1cc62853167b7183cc324a.png
# https://flyclipart.com/thumbs/vector-illustration-of-stratford-upon-avon-tudor-style-stratford-upon-avon-cartoon-1477652.png
# https://anvizbiometric.ru/wp-content/uploads/8/7/f/87f5629a6808640e69d2a39a127a7ab3.jpeg
# https://i.ytimg.com/vi/ULEprOna8-g/maxresdefault.jpg

import ffmpeg
import os
from time import sleep
from pathlib import Path
from threading import Thread
import logging
from entities import Slide
from data_storage import Video_List, append_test_video

PICS_DIR = "pics"
BASE_RESOLUTION = (1280, 720)
logger = logging.getLogger("app.main.ffmpeg")

# return size picture
def get_video_size(filename: str) -> tuple:
    try:
        logger.info("get_video_size for %s", filename)
        probe = ffmpeg.probe(filename)
        video_info = next(s for s in probe["streams"])  # if s["codec_type"] == "video")
        width = int(video_info["width"])
        height = int(video_info["height"])
        return width, height
    except ffmpeg.Error as e:
        logger.error(e)
        return 0


#  download and resize picture to make the same size before starting filter ffmpeg. New picture's size is not larger one of (base_size_x,base_size_y)
def load_and_resize_picture(
    *, input_url: str, output_dir: str, base_size_x=1280, base_size_y=720
) -> str:
    if len(input_url) and type(input_url) == str:
        file_out = input_url.split("/")[-1]  # take onli file name from url
    else:
        logger.error("len(input_url) and type(input_url) != str")
        return 0
    if not file_out:
        logger.error("load_and_resize_picture: cant split(/)")
        return 0
    name, ext = os.path.splitext(file_out)
    # logger.info("name %s, ext %s", name, ext)

    name += "_resize"
    # output_dir = "id111"  # REMOVE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    file_out = check_create_dir(output_dir) + "/" + name + ext
    pic_x, pic_y = get_video_size(input_url)
    scale = min(base_size_x / pic_x, base_size_y / pic_y)
    pic_x = int((scale * pic_x) + 0.5)
    pic_y = int((scale * pic_y) + 0.5)
    try:
        logger.info("load_and_resize_picture for %s", input_url)
        (  #  RECOMMENT FOR REAL USING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            ffmpeg.input(input_url)
            .filter("scale", pic_x, pic_y)
            .output(file_out, y="-y")
            .run()
        )
    except ffmpeg.Error as e:
        logger.error(e)
        return 0
    # start resize picture

    return file_out


# check and create dir for saving picture before resize
def check_create_dir(dir_name: str) -> str:
    dir_name = PICS_DIR + "/" + dir_name
    Path(dir_name).mkdir(parents=True, exist_ok=True)
    return dir_name


#  convert list of pictures to video with xfade ffmpeg. Argument is objects of Slide. Return url video
def convert_pic_to_video(slide: Slide) -> str:
    logger.info("start ffmpeg")
    if type(slide) != Slide:
        logging.error("convert_pic_to_video: type(slide) != Slide")
        return 0
    slide.status = "IN_PROGRESS"
    if len(slide.pics_list) < 2:
        slide.status = "ERROR"
        logging.error("convert_pic_to_video: len(slide.pics_list) < 2")
        return 0  # must be 2 or more pictures in slide, else cant make transition
    sum_offset = 0
    previous_pic = None
    for curr_pic in slide.pics_list:
        if previous_pic:  # pass first object in list
            file2 = load_and_resize_picture(
                input_url=curr_pic.srs, output_dir=slide.get_uid()
            )
            if not file2:
                logger.error("error load_and_resize_picture(file2)")
                slide.status = "ERROR"
                return 0
            if not sum_offset:  # only for 2 round of cycle
                file1 = load_and_resize_picture(
                    input_url=previous_pic.srs, output_dir=slide.get_uid()
                )
                if not file1:
                    logger.error("error load_and_resize_picture(file1)")
                    slide.status = "ERROR"
                    return 0
                faded = ffmpeg.input(file1, t=previous_pic.duration + 1, loop=1)
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
                return 0
            pass
        previous_pic = curr_pic
        pass

    # file_video = PICS_DIR + "/" + "id111" + "/video_out.mpg" FOR TEST local
    file_video = PICS_DIR + "/" + slide.get_uid() + "/video_out.mpg"
    try:
        logger.info("start making fade id = %s", slide.get_uid())
        out = (
            ffmpeg.output(faded, file_video, y="-y")
            .global_args("-loglevel", "error")
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as exc:
        logger.error("Error in making fade %s", slide.get_uid())
        logger.error(exc.stderr.decode("utf8"))
        logger.error(exc.stdout.decode("utf8"))
        slide.status = "ERROR"
        return 0
    slide.video_url = file_video
    slide.status = "READY"
    logger.info("Success making video id = %s", slide.get_uid())
    return 1


if __name__ == "__main__":
    ifile = "https://webmg.ru/wp-content/uploads/2022/10/i-17-15.jpeg"
    # print(load_and_resize_picture(input_url=ifile, output_dir="i12344321"))
    append_test_video()
    print(Video_List[0])
    print("*" * 50)
    print("******************START THREAD!!!!!!!!!!!!!!!!!!")
    th = Thread(target=convert_pic_to_video, args=(Video_List[0],))
    th.start()
    # convert_pic_to_video(Video_List[0])
    while th.is_alive():
        print("-----******-------")
        print(Video_List[0].status)
        sleep(0.1)
    print(Video_List[0])


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
