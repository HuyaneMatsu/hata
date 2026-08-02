from base64 import b64encode as base_64_encode

import vampytest
from scarletio.web_common import FormData

from ....attachment import Attachment
from ....attachment_request import (
    ATTACHMENT_REQUEST_WAVEFORM_OGG_DEFAULT, attachment_request_create_keep, attachment_request_copy_with_attachment_id,
    attachment_request_create_regular_create, attachment_request_create_voice_create
)

from ..attachments import CONVERSION_ATTACHMENTS, MESSAGE_FLAG_VOICE_MESSAGE

from .helpers import TestType


def _iter_options__set_validator():
    instance_0 = TestType('hey')
    instance_1 = TestType('there')
    
    # None
    yield (
        None,
        [
            None
        ],
    )
    
    # tuple
    yield (
        ('mister', instance_0),
        [[
            attachment_request_create_regular_create('mister', instance_0),
        ]],
    )
    
    # Attachment
    yield (
        Attachment.precreate(202403030000),
        [[
            attachment_request_create_keep(202403030000),
        ]],
    )
    
    # list
    yield (
        [
            instance_0,
            ('satori', instance_1),
            Attachment.precreate(202403030001),
        ],
        [[
            attachment_request_create_regular_create('hey', instance_0),
            attachment_request_copy_with_attachment_id(
                attachment_request_create_regular_create('satori', instance_1),
                1,
            ),
            attachment_request_create_keep(202403030001),
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
    output : ``list<None | list<AttachmentRequest>>``
    """
    return [*CONVERSION_ATTACHMENTS.set_validator(input_value)]


def _iter_options__serializer_putter():
    instance_0 = TestType('hey')
    
    yield (
        {},
        False,
        None,
        {},
    )
    
    yield (
        {},
        True,
        None,
        {
            'attachments': [],
        },
    )
    
    yield (
        {
            'flags': 2,
        },
        True,
        None,
        {
            'flags': 2,
            'attachments': [],
        },
    )
    
    yield (
        {},
        False,
        [
            attachment_request_create_keep(202403030002),
        ],
        {
            'attachments': [
                {
                    'id': str(202403030002),
                },
            ],
        },
    )
    
    yield (
        {
            'flags': 2,
        },
        False,
        [
            attachment_request_create_keep(202403030003),
        ],
        {
            'flags': 2,
            'attachments': [
                {
                    'id': str(202403030003),
                },
            ],
        },
    )
    
    form = FormData()
    form.add_json(
        'payload_json',
        {
            'attachments': [
                {
                    'id': str(0),
                },
            ],
        },
    )
    form.add_field(f'files[{0}]', instance_0, file_name = 'satori', content_type = 'application/octet-stream')
    yield (
        {},
        False,
        [
            attachment_request_create_regular_create('satori', instance_0),
        ],
        form,
    )
    
    # This may fail on older pythons, because of dict ordering
    form = FormData()
    form.add_json(
        'payload_json',
        {
            'flags': 2,
            'attachments': [
                {
                    'id': str(0),
                },
            ],
        },
    )
    form.add_field(f'files[{0}]', instance_0, file_name = 'satori', content_type = 'application/octet-stream')
    yield (
        {
            'flags': 2,
        },
        False,
        [
            attachment_request_create_regular_create('satori', instance_0),
        ],
        form,
    )
    
    # Voice attachment test.
    # This may fail on older pythons, because of dict ordering
    form = FormData()
    form.add_json(
        'payload_json',
        {
            'flags': 2 | MESSAGE_FLAG_VOICE_MESSAGE,
            'attachments': [
                {
                    'id': str(0),
                    'duration_secs': 2.0,
                    'waveform': base_64_encode(ATTACHMENT_REQUEST_WAVEFORM_OGG_DEFAULT).decode(),
                },
            ],
        },
    )
    form.add_field(f'files[{0}]', instance_0, file_name = 'satori.ogg', content_type = 'application/octet-stream')
    yield (
        {
            'flags': 2,
        },
        False,
        [
            attachment_request_create_voice_create('satori.ogg', instance_0, duration = 2.0),
        ],
        form,
    )


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
    
    value : ``None | list<AttachmentRequest>``
        The value to put into data.
    
    Returns
    -------
    output : ``dict<str, object> | FormData``
    """
    data = data.copy()
    return CONVERSION_ATTACHMENTS.serializer_putter(data, required, value)
