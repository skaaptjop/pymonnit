from .base import BaseEntity
from .fields import StringField, IntField, ReferenceField, UTCDateTimeField



class Network(BaseEntity):
    xml_tag = "APINetwork"
    id = IntField(xml_attribute="NetworkID")
    name = StringField(xml_attribute="NetworkName")


class Sensor(BaseEntity):
    xml_tag = "APISensor"
    id = IntField(xml_attribute="SensorID", query_param="sensorID")
    network = ReferenceField(Network, xml_attribute="CSNetID", query_param="NetworkID")
    name = StringField(xml_attribute="SensorName", query_param="Name")
    signal = IntField(xml_attribute="SignalStrength")
    battery = IntField(xml_attribute="BatteryLevel")


class Gateway(BaseEntity):
    """
    <APIGateway GatewayID="2599" NetworkID="100" Name="(103) gateway" GatewayType="Ethernet_Gateway"
                Heartbeat="5" IsDirty="False" LastCommunicationDate="1/11/2011 2:57:36 PM"
                LastInboundIPAddress="" />
    """
    xml_tag = "APIGateway"
    id = IntField(xml_attribute="GatewayID", query_param="gatewayID")
    network = ReferenceField(Network, xml_attribute="NetworkID", query_param="NetworkID")
    name = StringField(xml_attribute="Name", query_param="Name")
    type = StringField(xml_attribute="GatewayType")
    last = UTCDateTimeField(xml_attribute="LastCommunicationDate")