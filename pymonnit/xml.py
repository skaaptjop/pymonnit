from lxml import etree

#return self.xml_etree.xpath("/SensorRestAPI/Result[1]/text()='Success'")




class NetworkEntity(object):

    _xml_attrib_map = {"NetworkID": ("networkid", int),
                       "NetworkName": ("name", str)}

    def __init__(self, networkid, name):
        self.networkid = networkid
        self.name = name

    def __repr__(self):
        return "%s: %s" %(self.networkid, self.name)

    @classmethod
    def from_xml_attribs(cls, **kwargs):
        return cls(int(kwargs["NetworkID"]), kwargs["NetworkName"])





class Result(object):
    _entity_map = {"APINetwork": NetworkEntity}

    def __init__(self, xml_result):
        self.xml_result = xml_result

    @staticmethod
    def from_xml_string(xml_string):
        return Result.from_xml(etree.fromstring(xml_string))

    @staticmethod
    def from_xml(xml_response):
        result = xml_response.find("Result")
        return Result(result)

    def to_entity(self):
        if self.is_success():
            return True


    def __iter__(self):

        for child in self.xml_result.iterdescendants():
            if child.tag in self._entity_map:
                entityclass = self._entity_map[child.tag]
                yield entityclass.from_xml_attribs(**child.attrib)






    def is_success(self):
        return self.xml_result.text == "Success"