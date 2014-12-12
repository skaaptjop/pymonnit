import pymonnit

class MyEntity1(pymonnit.BaseEntity):
    id = pymonnit.IntField(xml_attribute="1_1_api_field")
    field_1_2 = pymonnit.IntField(xml_attribute="1_2_api_field", default=12)
    strfield = pymonnit.StringField(xml_attribute="apistrfield", min_length=3, default="pss")


class MyEntity2(pymonnit.BaseEntity):
    id = pymonnit.IntField(xml_attribute="apiid")
    ref = pymonnit.ReferenceField(MyEntity1, xml_attribute="refid")


e1 = MyEntity1(11)
#e1.strfield="do"
e1.validate()

e2 = MyEntity2(100, e1)
e2.validate()

e2.ref.strfield = "woooooot"
print e1.strfield


i=1


#
# username = "guest"
# password = "guest2014"
#
# proxy = pymonnit.MonnitProxy(username, password)
#
# #r = proxy.logon()
#
# response = """<?xml version="1.0" encoding="utf-8"?>
# <SensorRestAPI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
#   <Method>CreateNetwork2</Method>
#   <Result xsi:type="xsd:collection">
#     <APINetwork NetworkID="100" NetworkName="New Network Name" SendNotifications="True" />
#   </Result>
# </SensorRestAPI>"""
#
# response="""<?xml version="1.0" encoding="utf-8"?>
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
#
# x = pymonnit.Result.from_xml_string(response)
#
# for e in x:
#     print e
#
# i = 1