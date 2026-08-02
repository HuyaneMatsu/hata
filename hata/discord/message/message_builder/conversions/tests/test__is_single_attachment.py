import vampytest

from ....attachment import Attachment
from ....attachment_request import (
    AttachmentRequest, attachment_request_create_keep, attachment_request_create_regular_create
)

from ..attachments import _is_single_attachment

from .helpers import TestType


def _iter_options():
    instance_0 = TestType('hey')
    
    yield (
        (),
        [],
    )
    
    yield (
        Attachment.precreate(202402250000),
        [
            attachment_request_create_keep(202402250000),
        ],
    )
    
    yield (
        ('mister', instance_0),
        [
            attachment_request_create_regular_create('mister', instance_0),
        ],
    )
    
    yield (
        instance_0,
        [
            attachment_request_create_regular_create('hey', instance_0),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__is_single_attachment(input_value):
    """
    Tests whether ``_is_single_attachment`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test on.
    
    Returns
    -------
    output : ``list<AttachmentRequest>``
    """
    output = [*_is_single_attachment(input_value)]

    for element in output:
        vampytest.assert_instance(element, AttachmentRequest)
    
    return output
