from .fields import Field


class Schema:
    def __init__(self, pre_load=None, post_load=None):
        pass

    def load(self, data):
        for key, value in data.items():
            attr = getattr(self, key, None)
            if hasattr(self, key):
                if isinstance(attr, Field):
                    setattr(self, key, attr(value))
                elif isinstance(attr, Schema):
                    setattr(self, key, attr.load(value))

        return self
