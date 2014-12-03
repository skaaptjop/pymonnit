from lxml import etree

class MonnitXML(object):
    """Class encapsulating iMonnit XML responses"""

    def __init__(self, http_response):
        """
        Constructor
        :param http_response: XML string
        """
        #Build lxml.etree parsed XML from string
        self.xml_etree = etree.fromstring(http_response)


    @property
    def is_success_result(self):
        """
        :return: True if XML has <Result>Success</Result>
        """
        return self.xml_etree.xpath("/SensorRestAPI/Result[1]/text()='Success'")


    @property
    def root(self):
        """
        The root Element of the etree
        """
        return self.xml_etree
