
class Field:
    field_type = None

    def __init__(self, strict=False):
        self._strict = strict

    def __call__(self, value) -> field_type:
        try:
            return self.field_type(value)
        except TypeError:
            if self._strict:
                raise TypeError
            else:
                return None


class String(Field):
    field_type = str


class Integer(Field):
    field_type = int


class List(Field):

    def __init__(self, field=None, strict=False):
        super().__init__(strict)
        self.field = field

    def __call__(self, kwargs) -> list:
        return [self.field.load(item) for item in kwargs] if self.field else kwargs


class Nested(Field):

    def __init__(self, field, strict=False):
        super().__init__(strict)
        self.field = field

    def __call__(self, *args, **kwargs):
        return self.field.load(*args, **kwargs)
