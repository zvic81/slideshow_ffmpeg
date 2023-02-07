# Schemas for Marschmellow for validation and serialization data from endpoints to list of objects in memory
from apiflask import Schema, fields
from apiflask.validators import Range
from marshmallow import post_load
from entities import PictureSource


class BaseResponse(Schema):
    data = fields.Field()  # the data key
    code = fields.Integer()


class VideoOutSchema(Schema):
    _uid = fields.String()
    video_url = fields.String()
    status = fields.String()


class PictureSourceSchema(Schema):
    srs = fields.String(
        metadata={
            "example": "pics.com\\11/001.png"  # "https://cdn.pixabay.com/photo/2016/04/13/13/14/grass-1326759_960_720.jpg"
        }
    )
    duration = fields.Integer(
        required=True, validate=Range(min=1, max=59), metadata={"example": 5}
    )
    transition = fields.String(required=True, metadata={"example": "fade"})
    caption = fields.String(metadata={"example": "SuperShow"})

    @post_load
    def make_obj(self, data, **kwargs):  # название метода может быть любым
        return PictureSource(**data)


class VideoId(Schema):
    id = fields.String(required=True, metadata={"example": "xxd123123fsdf42342342"})

class VideoStatus(Schema):
    status = fields.String(required=True, metadata={"example": "READY"})
