from .base import Entity
from .fields import StringField, IntField, IDField

class Network(Entity):
    xml_tag = "APINetwork"
    id = IDField(xml_attribute="NetworkID")

    name = StringField(xml_attribute="NetworkName")