import vampytest

from ....attachment_request import AttachmentRequest, attachment_request_create_regular_create

from ..attachments import _is_valid_tuple_attachment

from .helpers import TestType


def _iter_options():
    instance_0 = TestType('mister')
    
    yield (
        (instance_0,),
        [
            attachment_request_create_regular_create('mister', instance_0),
        ],
    )
    
    yield (
        (None, instance_0,),
        [
            attachment_request_create_regular_create('mister', instance_0),
        ],
    )
    
    yield (
        ('hey', instance_0,),
        [
            attachment_request_create_regular_create('hey', instance_0),
        ],
    )
    
    yield (
        (None, instance_0, 'satori'),
        [
            attachment_request_create_regular_create('mister', instance_0, description = 'satori'),
        ],
    )
    
    yield (
        ('hey', instance_0, 'satori'),
        [
            attachment_request_create_regular_create('hey', instance_0, description = 'satori'),
        ],
    )
    
    yield (
        (),
        [],
    )
    
    yield (
        (None, instance_0, None, None),
        [],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__is_valid_tuple_attachment(input_value):
    """
    Tests whether ``_is_valid_tuple_attachment`` works as intended.
    
    Parameters
    ----------
    input_value : `tuple`
        Value to test on.
    
    Returns
    -------
    output : ``list<AttachmentRequest>``
    """
    output = [*_is_valid_tuple_attachment(input_value)]
    
    for element in output:
        vampytest.assert_instance(element, AttachmentRequest)
    
    return output
