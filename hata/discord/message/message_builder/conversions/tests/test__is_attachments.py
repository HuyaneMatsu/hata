from collections import OrderedDict

import vampytest

from ....attachment import Attachment
from ....attachment_request import (
    attachment_request_create_keep, attachment_request_copy_with_attachment_id, attachment_request_create_regular_create
)

from ..attachments import _is_attachments

from .helpers import TestType


def _iter_options():
    instance_0 = TestType('hey')
    instance_1 = TestType('there')
    
    # None
    yield (
        None,
        [None],
    )
    
    # tuple
    yield (
        (),
        [],
    )
    
    yield (
        ('mister', instance_0),
        [[
            attachment_request_create_regular_create('mister', instance_0),
        ]],
    )
    
    # Attachment
    yield (
        Attachment.precreate(202402250001),
        [[
            attachment_request_create_keep(202402250001),
        ]],
    )
    
    # list | Deque
    yield (
        [],
        [None],
    )
    yield (
        [
            instance_0,
            ('satori', instance_1),
            Attachment.precreate(202402250002),
        ],
        [[
            attachment_request_create_regular_create('hey', instance_0),
            attachment_request_copy_with_attachment_id(
                attachment_request_create_regular_create('satori', instance_1),
                1,
            ),
            attachment_request_create_keep(202402250002),
        ]]
    )
    
    # dict-like
    yield (
        OrderedDict([
            ('hey', instance_0),
            ('mister', instance_1),
        ]),
        [[
            attachment_request_create_regular_create('hey', instance_0),
            attachment_request_copy_with_attachment_id(
                attachment_request_create_regular_create('mister', instance_1),
                1,
            ),
        ]]
    )
    
    # rest
    yield (
        instance_0,
        [[
            attachment_request_create_regular_create('hey', instance_0),
        ]],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__is_attachments(input_value):
    """
    Tests whether ``_is_attachments`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test on.
    
    Returns
    -------
    output : ``list<None | list<AttachmentRequest>>``
    """
    output = [*_is_attachments(input_value)]
    return output
