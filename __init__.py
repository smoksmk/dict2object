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

    def __init__(self):

        fields = {}
        type_hints = T.get_type_hints(self, allow_forward=True)

        for name, hint in type_hints.items():
            if inspect.isclass(hint) and issubclass(hint, DataObject):
                fields[name] = FACTORIES[DataObject](hint)
            elif issubclass(type(hint), T._GenericAlias):
                fields[name] = FACTORIES[T.get_origin(hint)](T.get_args(hint)[0])
            else:
                pass

        self._fields = fields

    def load(self, data):
        self._data = data

        for name, value in data.items():
            if name in self._fields:
                value = self._fields[name]().load(value)

            setattr(self, name, value)

    @property
    def _existing(self):
        return 'id' in self._data


class Nested:
    def __init__(self, data_object, is_list=False):
        pass


FACTORIES = {
    list: list_factory,
    DataObject: proxy_factory,
}
