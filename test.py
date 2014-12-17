import pymonnit

proxy = pymonnit.MonnitClient("guest", "guest2014")

# r = proxy.query(pymonnit.Network).find()
#
# for i in r:
#     print i.id, i.name

# r = proxy.query(pymonnit.Network).get(2116)
# print r.id, r.name


# r = proxy.query(pymonnit.Sensor).get(39745)
# print r.id, r.name, r.network.id, r.network.name
#
rs = proxy.query(pymonnit.Sensor).find(network=2116)
for r in rs:
    print r.id, r.name, r.network.id, r.network.name, r.signal, r.battery

# rs = proxy.query(pymonnit.Sensor).find(name = "CO")
# for r in rs:
#     print r.id, r.name, r.network.id, r.network.name
# i = 1

r = proxy.query(pymonnit.Gateway).get(5039)
print r.id, r.name, r.network.id, r.network.name

rs = proxy.query(pymonnit.Gateway).find()
for r in rs:
    print r.id, r.name, r.network.id, r.network.name

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