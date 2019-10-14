from .fields import Field


class Schema:
    def __init__(self, pre_load=None, post_load=None, many=False):
        self._many = many

    def _prepare_data(self, data):
        for key, value in data.items():
            attr = getattr(self, key, None)
            if hasattr(self, key):
                if isinstance(attr, Field):
                    print('instance')
                    setattr(self, key, attr(value))
                elif isinstance(attr, Schema):
                    print('Schema', key, attr)
                    setattr(self, key, attr.load(value))

    def load(self, data):

        if self._many and isinstance(data, list):
            res = []
            for dt in data:
                res.append(self._prepare_data(dt))

            return res

        else:
            self._prepare_data(data)

        return self
