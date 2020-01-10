import inspect
import typing as T


def list_factory(data_object_class: 'DataObject'):
    def factory(data: list, **kwargs):
        return [data_object_class(data=item, **kwargs)for item in data]

    return factory


def proxy_factory(data_object_class):
    return data_object_class


class DataObject:
    _fields: dict

    def __init__(self, data: dict = None, extend=False):
        self._data = data
        if not data:
            data = {key: getattr(self, key) for key in self._fields.keys() if hasattr(self, key)}

        self.__load(data, extend)

    def __load(self, data, extend):
        for name, value in data.items():
            if name in self._fields:
                if inspect.isclass(self._fields.get(name)) and issubclass(self._fields.get(name), DataObject):
                    value = self._fields[name](value, extend=extend)
                else:
                    value = self._fields[name](value)
                setattr(self, name, value)
            elif extend:
                setattr(self, name, value)

    @classmethod
    def _resolve_type_hints(cls):
        fields = {}
        type_hints = T.get_type_hints(cls)

        for name, hint in type_hints.items():
            if inspect.isclass(hint) and issubclass(hint, DataObject):
                fields[name] = FACTORIES[DataObject](hint)
            elif issubclass(type(hint), T._GenericAlias):
                fields[name] = FACTORIES[T.get_origin(hint)](T.get_args(hint)[0])
            elif hint in (str, int, bool):
                fields[name] = hint
            else:
                pass

        cls._fields = fields

    def __dictify(self, name, value):

        if isinstance(value, DataObject):
            return {name: value.get_dict()}
        elif isinstance(value, list):
            return {name: [self.__dictify(name, i) for i in value]}
        else:
            return {name: value}

    def get_dict(self):
        fields = {}
        for name, value in self.__dict__.items():
            if not name.startswith('_') and not name.startswith('get_'):
                fields.update(self.__dictify(name, value))
        return fields


FACTORIES = {
    list: list_factory,
    DataObject: proxy_factory,
}
