# for test put in console pytest -s -v -m ffmpeg
# need installed pytest and pytest-mock to venv!!!

import pytest
import sys
import os.path
import shutil

from pathlib import Path
from apiflask import APIFlask
app_dir = (os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..')) + '/srs/')
sys.path.append(app_dir)
import ffmpeg_function
import entities
from data_storage import create_video_object
import app

PIC_DIR = 'tests/pics'


@pytest.mark.ffmpeg
def test_get_video_size():
    pic_url = video_url = Path(PIC_DIR + "/001.png")
    res = ffmpeg_function.get_video_size(pic_url)
    assert res == (360, 640)


@pytest.mark.ffmpeg
def test_load_and_resize_picture(mocker):
    pic_url = os.path.abspath(os.path.join(os.path.dirname(
        __file__), '..')) + '/' + PIC_DIR + '/i000000048.png'
    mocker.patch('ffmpeg_function.check_create_dir',
                 return_value='/home/vic/python/slideshow_ffmpeg/tests/pics')
    res = ffmpeg_function.load_and_resize_picture(
        input_url=pic_url, output_dir='1', count_file_name=111)
    assert '/tests/pics/111.png' in res
    assert os.path.isfile(res)
    os.remove(res)
    pass


@pytest.mark.ffmpeg
def test_convert_pic_to_video(mocker):
    app.init_logger("app")
    app.init_dir()
    import data_storage
    data_pic = [entities.PictureSource(
        'pic1', 3, 'fade', '2'), entities.PictureSource('pic1', 3, 'fade', '2'),]
    new_video = create_video_object(
        status="NEW", video_url="None", picture_list=data_pic)
    mocker.patch('ffmpeg_function.load_and_resize_picture', side_effect=[
                 '/home/vic/python/slideshow_ffmpeg/tests/pics/frame1.png', '/home/vic/python/slideshow_ffmpeg/tests/pics/frame2.png'])
    mocker.patch('ffmpeg_function.move_video_to_firebase', return_value=0)
    pic_url = os.path.abspath(os.path.join(os.path.dirname(
        __file__), '..')) + '/' + PIC_DIR
    dir_name = pic_url + '/' + new_video.get_uid()
    Path(dir_name).mkdir(parents=True, exist_ok=True)

    mocker.patch.object(data_storage, 'PICS_DIR', pic_url)
    res = ffmpeg_function.convert_pic_to_video(new_video)
    assert res == 0
    video_url = Path(dir_name + '/' + "/video_out.mpg")
    assert video_url.is_file() == True
    shutil.rmtree(Path(dir_name))

    pass
