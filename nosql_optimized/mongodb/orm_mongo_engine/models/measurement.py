from mongoengine import *

class Sensor(EmbeddedDocument):
    id = IntField()
    parameter = StringField()

class Location(EmbeddedDocument):
    id = IntField()
    city = StringField()
    country = StringField()
    lat = FloatField()
    lon = FloatField()

class Measurement(Document):
    timestamp = DateTimeField()
    value = FloatField()

    sensor = EmbeddedDocumentField(Sensor)
    location = EmbeddedDocumentField(Location)

    meta = {"collection": "measurements"}
