import vampytest

from ..attachment import Attachment
from ..flags import AttachmentFlag

from .test__Attachment__constructor import _assert_fields_set


def test__Attachment__from_data():
    """
    Tests whether ``Attachment.from_data`` works as intended.
    
    Case: default.
    """
    attachment_id = 202211010004
    content_type = 'application/json'
    description = 'Nue'
    duration = 12.6
    flags = AttachmentFlag(12)
    height = 1000
    name = 'i miss you'
    size = 999
    proxy_url = 'https://orindance.party/'
    temporary = True
    title = 'flandre'
    url = 'https://www.astil.dev/'
    waveform = 'kisaki'
    width = 998
    
    data = {
        'id': str(attachment_id),
        'content_type': content_type,
        'description': description,
        'duration_sec': duration,
        'flags': int(flags),
        'height': height,
        'filename': name,
        'size': size,
        'proxy_url': proxy_url,
        'ephemeral': temporary,
        'title': title,
        'url': url,
        'waveform': waveform,
        'width': width,
    }
    
    attachment = Attachment.from_data(data)
    
    _assert_fields_set(attachment)
    
    vampytest.assert_eq(attachment.id, attachment_id)
    vampytest.assert_eq(attachment.proxy_url, proxy_url)

    vampytest.assert_eq(attachment.content_type, content_type)
    vampytest.assert_eq(attachment.description, description)
    vampytest.assert_eq(attachment.duration, duration)
    vampytest.assert_eq(attachment.flags, flags)
    vampytest.assert_eq(attachment.height, height)
    vampytest.assert_eq(attachment.name, name)
    vampytest.assert_eq(attachment.size, size)
    vampytest.assert_eq(attachment.temporary, temporary)
    vampytest.assert_eq(attachment.title, title)
    vampytest.assert_eq(attachment.url, url)
    vampytest.assert_eq(attachment.waveform, waveform)
    vampytest.assert_eq(attachment.width, width)


def test__Attachment__to_data():
    """
    Tests whether ``Attachment.to_data`` works as intended.
    
    Case: include defaults & internals.
    """
    attachment_id = 202211010005
    content_type = 'application/json'
    description = 'Nue'
    duration = 12.6
    flags = AttachmentFlag(12)
    height = 1000
    name = 'i miss you'
    size = 999
    proxy_url = 'https://orindance.party/'
    temporary = True
    title = 'flandre'
    url = 'https://www.astil.dev/'
    waveform = 'kisaki'
    width = 998
    
    attachment = Attachment.precreate(
        attachment_id,
        content_type = content_type,
        description = description,
        duration = duration,
        flags = flags,
        height = height,
        name = name,
        proxy_url = proxy_url,
        size = size,
        temporary = temporary,
        title = title,
        url = url,
        waveform = waveform,
        width = width,
    )
    
    vampytest.assert_eq(
        attachment.to_data(
            defaults = True,
            include_internals = True,
        ),
        {
            'id': str(attachment_id),
            'content_type': content_type,
            'description': description,
            'duration_sec': duration,
            'flags': int(flags),
            'height': height,
            'filename': name,
            'size': size,
            'proxy_url': proxy_url,
            'ephemeral': temporary,
            'title': title,
            'url': url,
            'waveform': waveform,
            'width': width,
        },
    )
