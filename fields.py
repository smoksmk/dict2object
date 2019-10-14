from abc import ABC


class Field(ABC):
    field_type = None

    def __init__(self, strict=False):
        self._strict = strict

    def __call__(self, value):
        try:
            return self.field_type(value)
        except TypeError:
            raise TypeError if self._strict else None

    def __repr__(self):
        return ','.join(self.__dict__)


class String(Field):
    field_type = str


class Integer(Field):
    field_type = int


class List(Field):
    field_type = list


class Nested(Field):
    field_type = dict

    def __init__(self, field, strict=False):
        super().__init__(strict)
        self.field = field

    def __call__(self, *args, **kwargs):
        return self.field().load(*args, **kwargs)
