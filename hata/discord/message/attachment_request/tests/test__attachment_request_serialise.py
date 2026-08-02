from base64 import b64encode as base_64_encode

import vampytest

from ..constants import ATTACHMENT_REQUEST_WAVEFORM_OGG_DEFAULT
from ..utils import (
    attachment_request_create_regular_create, attachment_request_create_regular_edit,
    attachment_request_create_video_create, attachment_request_create_keep, attachment_request_create_video_edit,
    attachment_request_create_voice_create, attachment_request_create_voice_edit, attachment_request_serialise
)


def _iter_options():
    attachment_id = 202607070020
    io = b'nyan'
    name = 'rin.ogg'
    duration = 2.0
    description = 'hell cat'
    spoiler = True
    title = 'rin'
    waveform = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    
    # Creations
    
    yield (
        'regular create thin',
        attachment_request_create_regular_create(name, io),
        {
            'id': '0',
        },
    )
    
    yield (
        'regular create thick',
        attachment_request_create_regular_create(name, io, description = description, spoiler = spoiler, title = title),
        {
            'id': '0',
            'description': description,
            'is_spoiler': spoiler,
            'title': title,
        },
    )
    
    yield (
        'voice create thin',
        attachment_request_create_voice_create(name, io, duration),
        {
            'id': '0',
            'duration_secs': duration,
            'waveform': base_64_encode(ATTACHMENT_REQUEST_WAVEFORM_OGG_DEFAULT).decode(),
        },
    )
    
    yield (
        'voice create think',
        attachment_request_create_voice_create(name, io, duration, description = description, waveform = waveform),
        {
            'id': '0',
            'duration_secs': duration,
            'description': description,
            'waveform': base_64_encode(waveform).decode(),
        },
    )
    
    yield (
        'video create thin',
        attachment_request_create_video_create(name, io, duration),
        {
            'id': '0',
            'duration_secs': duration,
        },
    )
    
    yield (
        'video create think',
        attachment_request_create_video_create(name, io, duration, description = description),
        {
            'id': '0',
            'duration_secs': duration,
            'description': description,
        },
    )
    
    # Editions
    
    yield (
        'regular edit thin',
        attachment_request_create_regular_edit(attachment_id),
        {
            'id': str(attachment_id),
        },
    )
    
    yield (
        'regular edit thick',
        attachment_request_create_regular_edit(attachment_id, description = description, spoiler = spoiler),
        {
            'id': str(attachment_id),
            'description': description,
            'is_spoiler': spoiler,
        },
    )
    
    yield (
        'voice edit thin',
        attachment_request_create_voice_edit(attachment_id),
        {
            'id': str(attachment_id),
        },
    )
    
    yield (
        'voice edit think',
        attachment_request_create_voice_edit(attachment_id, description = description),
        {
            'id': str(attachment_id),
            'description': description,
        },
    )
    
    yield (
        'video edit thin',
        attachment_request_create_video_edit(attachment_id),
        {
            'id': str(attachment_id),
        },
    )
    
    yield (
        'video edit think',
        attachment_request_create_video_edit(attachment_id, description = description),
        {
            'id': str(attachment_id),
            'description': description,
        },
    )
    
    # Keep (edition)
    
    yield (
        'keep',
        attachment_request_create_keep(attachment_id),
        {
            'id': str(attachment_id),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__attachment_request_serialise(attachment_request):
    """
    Tests whether ``attachment_request_serialise`` works as intended.
    
    Parameters
    ----------
    attachment_request : ``AttachmentRequest``
        Instance to serialise.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    output = attachment_request_serialise(attachment_request)
    vampytest.assert_instance(output, dict)
    return output
