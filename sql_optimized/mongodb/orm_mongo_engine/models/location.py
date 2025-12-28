from mongoengine import Document, StringField, FloatField, IntField

class Location(Document):
    meta = {"collection": "locations"}

    id = IntField(primary_key=True)
    city = StringField()
    country = StringField()
    latitude = FloatField()
    longitude = FloatField()
