import pymonnit


class MyEntity1(pymonnit.Entity):
    field_1_1 = pymonnit.BaseField("1_1_api_field", key=True)
    field_1_2 = pymonnit.BaseField("1_2_api_field", default=12, key=True)
    strfield = pymonnit.StringField(xml_attribute="apistrfield", min_length=3, default="pss")

    meta = {"xml_tag": "thetagytag"}


e1 = MyEntity1(11)
#e1.strfield="do"
e1.validate()

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