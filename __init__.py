from .fields import Field


class Schema:
    def __init__(self, proxy_class=None):
        pass

    def _prepare_data(self, data):
        for key, value in data.items():
            attr = getattr(self, key, None)
            if hasattr(self, key):
                if isinstance(attr, Field):
                    setattr(self, key, attr(value))

    def load(self, data) -> (dict, list):
        self._prepare_data(data)
        return self

    def __repr__(self):
        attr = ', '.join(self.__dict__)
        return f'{self.__class__.__name__} has attr: ({attr})'
