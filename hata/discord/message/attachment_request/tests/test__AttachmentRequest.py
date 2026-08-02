import vampytest

from ..attachment_request import AttachmentRequest
from ..constants import ATTACHMENT_REQUEST_ACTION_CREATE, ATTACHMENT_REQUEST_TYPE_REGULAR, ATTACHMENT_REQUEST_TYPE_VOICE


def _assert_fields_set(attachment_request):
    """
    Asserts whether all fields are set of the given attachment request.
    
    Parameters
    ----------
    attachment_request : ``AttachmentRequest``
        Instance to test.
    """
    vampytest.assert_instance(attachment_request, AttachmentRequest)
    vampytest.assert_instance(attachment_request.attachment_id, int)
    vampytest.assert_instance(attachment_request.attachment_request_flags, int)
    vampytest.assert_instance(attachment_request.description, str, nullable = True)
    vampytest.assert_instance(attachment_request.duration, float)
    vampytest.assert_instance(attachment_request.io, object, nullable = True)
    vampytest.assert_instance(attachment_request.name, str, nullable = True)
    vampytest.assert_instance(attachment_request.spoiler, bool)
    vampytest.assert_instance(attachment_request.title, str, nullable = True)
    vampytest.assert_instance(attachment_request.waveform, bytes, nullable = True)
    

def test__AttachmentRequest__new():
    """
    Tests whether ``AttachmentRequest.__new__`` works as intended.
    """
    attachment_id = 202607070000
    attachment_request_flags = ATTACHMENT_REQUEST_ACTION_CREATE | ATTACHMENT_REQUEST_TYPE_REGULAR
    description = 'hell cat'
    duration = 2.0
    io = b'nyan'
    name = 'rin.txt'
    spoiler = True
    title = 'orin'
    waveform = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    
    attachment_request = AttachmentRequest(
        attachment_request_flags,
        attachment_id,
        io,
        name,
        title,
        description,
        spoiler,
        duration,
        waveform,
    )
    _assert_fields_set(attachment_request)
    
    vampytest.assert_eq(attachment_request.attachment_id, attachment_id)
    vampytest.assert_eq(attachment_request.attachment_request_flags, attachment_request_flags)
    vampytest.assert_eq(attachment_request.description, description)
    vampytest.assert_eq(attachment_request.duration, duration)
    vampytest.assert_eq(attachment_request.io, io)
    vampytest.assert_eq(attachment_request.name, name)
    vampytest.assert_eq(attachment_request.spoiler, spoiler)
    vampytest.assert_eq(attachment_request.title, title)
    vampytest.assert_eq(attachment_request.waveform, waveform)
    

def test__AttachmentRequest__repr():
    """
    Tests whether ``AttachmentRequest.__repr__`` works as intended.
    """
    attachment_id = 202607070002
    attachment_request_flags = ATTACHMENT_REQUEST_ACTION_CREATE | ATTACHMENT_REQUEST_TYPE_REGULAR
    description = 'hell cat'
    duration = 2.0
    io = b'nyan'
    name = 'rin.txt'
    spoiler = True
    title = 'orin'
    waveform = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    
    attachment_request = AttachmentRequest(
        attachment_request_flags,
        attachment_id,
        io,
        name,
        title,
        description,
        spoiler,
        duration,
        waveform,
    )
    _assert_fields_set(attachment_request)
    
    output = repr(attachment_request)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    attachment_id = 202607070003
    attachment_request_flags = ATTACHMENT_REQUEST_ACTION_CREATE | ATTACHMENT_REQUEST_TYPE_REGULAR
    description = 'hell cat'
    duration = 2.0
    io = b'nyan'
    name = 'rin.txt'
    spoiler = True
    title = 'orin'
    waveform = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    
    keyword_parameters = {
        'attachment_request_flags': attachment_request_flags,
        'attachment_id': attachment_id,
        'io': io,
        'name': name,
        'title': title,
        'description': description,
        'spoiler': spoiler,
        'duration': duration,
        'waveform': waveform,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'attachment_request_flags': ATTACHMENT_REQUEST_ACTION_CREATE | ATTACHMENT_REQUEST_TYPE_VOICE,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'attachment_id': 4,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'io': 'rawr',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'name': 'okuu.txt',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'title': 'unyu',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'description': 'bord',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'spoiler': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'duration': 2.23,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'waveform': None,
        },
        False,
    )



@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__AttachmentRequest__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``AttachmentRequest.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    attachment_request_0 = AttachmentRequest(**keyword_parameters_0)
    attachment_request_1 = AttachmentRequest(**keyword_parameters_1)
    
    output = attachment_request_0 == attachment_request_1
    vampytest.assert_instance(output, bool)
    return output
