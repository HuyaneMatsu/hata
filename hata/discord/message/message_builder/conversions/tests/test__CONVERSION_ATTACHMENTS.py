import vampytest
from scarletio.web_common import FormData

from ....attachment import Attachment

from ..attachments import CONVERSION_ATTACHMENTS


class TestType():
    __slots__ = ('name')
    
    def __new__(cls, name):
        self = object.__new__(cls)
        self.name = name
        return self


def _iter_options__set_validator():
    instance_0 = TestType('hey')
    instance_1 = TestType('there')
    
    # None
    yield None, [None]
    
    # tuple
    yield ('mister', instance_0), [[(False, ('mister', instance_0, None))]]
    
    # Attachment
    yield Attachment.precreate(202403030000), [[(True, 202403030000)]]
    
    # list
    yield (
        [
            instance_0,
            ('satori', instance_1),
            Attachment.precreate(202403030001),
        ],
        [[
            (False, ('hey', instance_0, None)),
            (False, ('satori', instance_1, None)),
            (True, 202403030001)
        ]]
    )


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_ATTACHMENTS__set_validator(input_value):
    """
    Tests whether ``CONVERSION_ATTACHMENTS.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<None | list<(bool<True>, int) | (bool<False>, (str, object, None | str))>>`
    """
    return [*CONVERSION_ATTACHMENTS.set_validator(input_value)]


def _iter_options__serializer_putter():
    instance_0 = TestType('hey')
    
    yield {}, False, None, {}
    yield {}, True, None, {'attachments': []}
    yield {'flags': 2}, True, None, {'flags': 2, 'attachments': []}
    yield {}, False, [(True, 202403030002)], {'attachments': [{'id': str(202403030002)}]}
    yield {'flags': 2}, False, [(True, 202403030003)], {'flags': 2, 'attachments': [{'id': str(202403030003)}]}
    
    form = FormData()
    form.add_json('payload_json', {'attachments': [{'id': str(0)}]})
    form.add_field(f'files[{0}]', instance_0, file_name = 'satori', content_type = 'application/octet-stream')
    yield {}, False, [(False, ('satori', instance_0, None))], form
    
    # This may fail on older pythons, because of dict ordering
    form = FormData()
    form.add_json('payload_json', {'flags': 2, 'attachments': [{'id': str(0)}]})
    form.add_field(f'files[{0}]', instance_0, file_name = 'satori', content_type = 'application/octet-stream')
    yield {'flags': 2}, False, [(False, ('satori', instance_0, None))], form


@vampytest._(vampytest.call_from(_iter_options__serializer_putter()).returning_last())
def test__CONVERSION_ATTACHMENTS__serializer_putter(data, required, value):
    """
    Tests whether ``CONVERSION_ATTACHMENTS.serializer_putter`` works as intended.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to serialize.
    required : `bool`
        Whether this field is required.
    value : `None | list<(bool<True>, int) | (bool<False>, (str, object, None | str))>`
        The value to put into data.
    
    Returns
    -------
    output : `dict<str, object> | FormData`
    """
    data = data.copy()
    return CONVERSION_ATTACHMENTS.serializer_putter(data, required, value)
