from mongoengine import Document, IntField, StringField

class Sensor(Document):
    meta = {"collection": "sensors"}

    id = IntField(primary_key=True)
    location_id = IntField()
    parameter = StringField()
