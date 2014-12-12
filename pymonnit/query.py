

class Query(object):
    def __init__(self, qclass, **qargs):
        self._entity_class = qclass
        self._query_args = qargs




from .entity import *
q = Query(Network, id=1)

i = 1