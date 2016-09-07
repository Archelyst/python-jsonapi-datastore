from collections import defaultdict


__version__ = '0.1.2'


class JsonApiDataStoreModel:
    def __init__(self, _type, _id):
        self.id = _id
        self._type = _type
        self._attributes = []
        self._relationships = []
        self._place_holder = False

    def __repr__(self):
        return '{type: %s, id: %s}' % (self._type, self.id)


class JsonApiDataStore:
    def __init__(self):
        self.graph = defaultdict(dict)

    def destroy(self, model):
        """Remove a model from the store."""
        del self.graph[model._type][model.id]

    def find(self, _type, _id):
        """Retrieve a model by type and id. Constant-time lookup."""
        if _type in self.graph and _id in self.graph[_type]:
            return self.graph[_type][_id]

    def find_all(self, _type):
        """Retrieve all models by type."""
        if _type not in self.graph:
            return []
        return list(self.graph[_type].values())

    def reset(self):
        """Empty the store."""
        self.graph = {}

    def init_model(self, _type, _id):
        _id = str(_id)
        if _id not in self.graph[_type]:
            self.graph[_type][_id] = JsonApiDataStoreModel(_type, _id)
        return self.graph[_type][_id]

    def syncRecord(self, record):
        model = self.init_model(record['type'], record['id'])
        model._place_holder = False

        for key, value in record['attributes'].items():
            model._attributes.append(key)
            setattr(model, key, value)

        if 'relationships' in record:
            for rel_name, rel in record['relationships'].items():
                if 'data' in rel:
                    data = rel['data']
                    model._relationships.append(rel_name)
                    if data is None:
                        setattr(model, rel_name, None)
                    elif type(data) == list:
                        setattr(model, rel_name, [self._findOrInit(rec for rec in data)])
                    else:
                        setattr(model, rel_name, self._findOrInit(data))
        return model

    def _findOrInit(self, record):
        _id = str(record['id'])
        if record['type'] not in self.graph or _id not in self.graph[record['type']]:
            place_holder_model = self.init_model(record['type'], _id)
            place_holder_model._place_holder = True
        return self.graph[record['type']][_id]

    def syncWithMeta(self, payload):
        """
        Sync a JSONAPI-compliant payload with the store and return any metadata included in
        the payload.

        :return The model/list of models corresponding to the payload's primary resource(s)
                and any metadata.
        """
        primary = payload['data']
        if not primary:
            return []
        if 'included' in payload:
            for record in payload['included']:
                self.syncRecord(record)
        if type(primary) == list:
            data = [self.syncRecord(record) for record in primary]
        else:
            data = self.syncRecord(primary)
        return {'data': data, 'meta': payload['meta'] if 'meta' in payload else None}

    def sync(self, payload):
        """
        Sync a JSONAPI-compliant payload with the store.

        :return The model/array of models corresponding to the payload's primary resource(s).
        """
        return self.syncWithMeta(payload)['data']
