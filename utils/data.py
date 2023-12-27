import typing
import unittest


def _data_inject_into_method(method: typing.Callable, *args, **kwargs) -> typing.Callable:
    def wrapper(self):
        return method(self, *args, **kwargs)

    return wrapper


def data_driven(cls: unittest.TestCase) -> unittest.TestCase:
    """ class decorator for ``unittest.TestCase`` or its subclasses """

    for name, method in list(cls.__dict__.items()):
        if hasattr(method, 'data-driven'):
            for index, value in enumerate(getattr(method, 'data-driven')):
                if isinstance(value, dict):
                    method_injected_data = _data_inject_into_method(method, **value)
                elif isinstance(value, (list, tuple)):
                    method_injected_data = _data_inject_into_method(method, *value)
                else:
                    method_injected_data = _data_inject_into_method(method, value)

                method_injected_data.__doc__ = f'{md.strip() if (md := method.__doc__) else ""}(data: {value})'
                setattr(cls, f'{name}_{index + 1}', method_injected_data)
            else:
                delattr(cls, name)

    return cls


def data_inject(data: typing.Iterable) -> typing.Callable:
    """ method decorator for test methods of ``unittest.TestCase`` or its subclasses """

    def wrapper(method):
        setattr(method, 'data-driven', data)
        return method

    return wrapper
