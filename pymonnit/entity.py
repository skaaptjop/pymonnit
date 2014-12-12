from .base import BaseEntity
from .fields import StringField, IntField



class Network(BaseEntity):
    xml_tag = "APINetwork"
    id = IntField(xml_attribute="NetworkID")
    name = StringField(xml_attribute="NetworkName")


