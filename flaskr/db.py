
#type: ignore
from typing import Any
import click
from flask import current_app, g
from flask.cli import with_appcontext
from flaskext.couchdb import *


class HouseObject(Document):
    doc_type = 'housedata'

    house_id = IntegerField()
    house_type = TextField()
    build_year = IntegerField()
    house_size = FloatField()
    bedrooms_no = IntegerField()
    country = TextField()
    energy_data = ListField(DictField(Mapping.build(
        local_minute = DateTimeField(),
        air1 = FloatField(),
        bedroom1 = FloatField(),
        bedroom2 = FloatField(),
        clotheswasher1 = FloatField(),
        dishwasher1 = FloatField(),
        disposal1 = FloatField(),
        dryer1 = FloatField(),
        furnace1 = FloatField(),
        grid = FloatField(),
        kitchenapp1 = FloatField(),
        kitchenapp2 = FloatField(),
        lights_plugs1 = FloatField(),
        microwave1 = FloatField(),
        refrigerator1 = FloatField(),
        leg1v = FloatField(),
        leg2v = FloatField()
    )))
