#from lxml import etree
import xml.etree.ElementTree as ET

# import inspect
# def entity_finder(e):
#     return inspect.isclass(e) and issubclass(e, entity.BaseEntity) and e is not entity.BaseEntity
#
# entity_map = {fo.xml_tag:fn for fn, fo in inspect.getmembers(entity, entity_finder)}



class ResultSet(object):
    def __init__(self, results):
        self._results = results

    def __getitem__(self, item):
        return self._results[item]

    def __len__(self):
        return len(self._results)

    def __contains__(self, item):
        if isinstance(item, int):
            item_ = item
        else:
            item_ = item.id
        return item_ in (r.id for r in self._results)

    def __iter__(self):
        return iter(self._results)

    def all(self):
        return list(self._results)

    def first(self):
        try:
            result = self._results[0]
        except KeyError:
            result = None
        return result


def from_xml(entity_class, xml_string):
    xml_root = ET.fromstring(xml_string).find("Result")
    results = []
    for i in xml_root.iterfind((".//" + entity_class.xml_tag)):
        e = entity_class.from_xml(i)
        results.append(e)
    # results = map(entity_class.from_xml, xml_root.iterfind((".//" + entity_class.xml_tag)))
    return ResultSet(results)


def is_success(xml_string):
    """
    Does the XML simply contain  <Result>Success</Result>?
    """
    return ET.fromstring(xml_string).find("Result").text == "Success"



# xml = """<?xml version="1.0" encoding="utf-8"?>
# <SensorRestAPI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
#   <Method>NetworkList</Method>
#   <Result xsi:type="xsd:collection">
#     <APINetworkList>
#       <APINetwork NetworkID="100" NetworkName="OfficeNetwork" SendNotifications="False" />
#       <APINetwork NetworkID="300" NetworkName="Warehouse" SendNofitications="True" />
#     </APINetworkList>
#   </Result>
# </SensorRestAPI>"""
#
# rs = from_xml(MyNetwork, xml)
#
# xml = """<?xml version="1.0" encoding="utf-8"?>
# <SensorRestAPI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
#   <Method>NetworkList</Method>
#   <Result xsi:type="xsd:collection">Success</Result></SensorRestAPI>
#   """
#
#
# print is_success(xml)
#
#
# for r in rs:
#     print r
#
# a = rs.all()
#
# print 300 in rs
# i = 1
