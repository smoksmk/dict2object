class Field:
    def __call__(self, value):
        return value

    def __repr__(self):
        return ','.join(self.__dict__)


class String(Field):
    pass


class Integer(Field):
    pass


class Nested(Field):
    def __init__(self, field):
        self.field = field

    def __call__(self, *args, **kwargs):
        return self.field().load(*args, **kwargs)
