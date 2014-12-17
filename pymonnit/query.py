from .exceptions import QueryError
from .entity import Network, Sensor, Gateway

import xml.etree.ElementTree as ET


class ResultSet(list):
    def all(self):
        return self

    def first(self):
        try:
            result = self[0]
        except IndexError:
            result = None
        return result

    @staticmethod
    def from_xml(entity_class, xml_string):
        """
        Create a ResultSet of entities populated with field values from the XML response.
        """
        xml_root = ET.fromstring(xml_string).find("Result")
        results = map(entity_class.from_xml, xml_root.iterfind((".//" + entity_class.xml_tag)))
        return ResultSet(results)


def is_success(xml_string):
    """
    Does the XML simply contain  <Result>Success</Result>?
    """
    return ET.fromstring(xml_string).find("Result").text == "Success"


class Query(object):
    def __init__(self, client):
        """
        Query Constructor (base).
        :param client: MonnitClient instance
        """
        self._client = client

    def find(self, **query_args):
        raise NotImplementedError

    def get(self, entity_id):
        raise NotImplementedError

    def _query(self, entity, method, **query_args):
        params = self._build_http_query_params(entity, **query_args)
        xml = self._client.execute(method, params)
        return ResultSet.from_xml(entity, xml)

    def _check_query_filter(self, entity, **query_params):
        invalid_params = set(query_params) - entity.meta["queryable_fields"]
        if invalid_params:
            raise QueryError("Can't query on field '%s' (no query_param set on entity)" % invalid_params.pop())

    def _build_http_query_params(self, entity, **query_args):
        """
        Convert field names into their API query parameter equivalents, e.g.
        finding by 'id' on the Network entity should resolve to 'networkID' by HTTP query parameter.
        :param entity: Entity class
        :param query_args: field name - values to filter
        If a query arg (field name) is supplied that does not have a configured 'query_param' attribute associated
        with the field descripter then a QueryError is raised.
        """
        self._check_query_filter(entity, **query_args)
        http_params = {}
        for key, value in query_args.items():
            http_params[entity.meta["field_name_to_query_param"][key]] = value
        return http_params

    def _derefence_network(self, result_set):
        """
        Populate entities with network entities for reference fields
        """
        network_cache = {}
        for entity in result_set:
            network_id = entity.network
            network = network_cache.get(network_id)
            if network is None:
                network = self._client.query(Network).get(network_id)
                network_cache[network_id] = network
            entity.network = network
        return result_set


class NetworkQuery(Query):
    def find(self, **query_args):
        return self._query(Network, "NetworkList", **query_args)

    def get(self, entity_id):
        networks = self.find()
        for network in networks:
            if network.id == entity_id:
                return network
        return None


class SensorQuery(Query):
    def get(self, entity_id):
        sensors = self._query(Sensor, "SensorGet", id=entity_id)
        sensors = self._derefence_network(sensors)
        return sensors.first()

    def find(self, **query_args):
        sensors = self._query(Sensor, "SensorList", **query_args)
        sensors = self._derefence_network(sensors)
        return sensors


class GatewayQuery(Query):
    def get(self, entity_id):
        gateways = self._query(Gateway, "GatewayGet", id=entity_id)
        gateways = self._derefence_network(gateways)
        return gateways.first()

    def find(self, **query_args):
        gateways = self._query(Gateway, "GatewayList", **query_args)
        gateways = self._derefence_network(gateways)
        return gateways


_entity_query_map = {Network: NetworkQuery,
                     Sensor: SensorQuery,
                     Gateway: GatewayQuery}


def get_query(entity_class, proxy):
    """
    Factory that returns the entity specific query class
    :param entity_class: entity class, e.g. Network
    :param proxy: Monnit proxy instance
    :return: entity specific query class, e.g. NetworkQuery
    """
    try:
        return _entity_query_map[entity_class](proxy)
    except KeyError:
        raise QueryError("Unknown entity class")
