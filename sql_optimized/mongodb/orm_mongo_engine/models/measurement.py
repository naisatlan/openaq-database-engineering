from mongoengine import Document, IntField, FloatField, DateTimeField

class Measurement(Document):
    meta = {"collection": "measurements"}

    sensor_id = IntField()
    value = FloatField()
    timestamp = DateTimeField()
