from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....application import Application
from ....user import User

from ..attachment import Attachment
from ..flags import AttachmentFlag


def test__Attachment__repr():
    """
    Tests whether ``Attachment.__repr__`` works as intended.
    """
    application = Application.precreate(202502020009)
    attachment_id = 202211010006
    clip_created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    clip_users = [
        User.precreate(202502020028),
        User.precreate(202502020029),
    ]
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
    width = 998
    
    attachment = Attachment.precreate(
        attachment_id,
        application = application,
        clip_created_at = clip_created_at,
        clip_users = clip_users,
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
        width = width,
    )
    
    vampytest.assert_instance(repr(attachment), str)


def test__Attachment__hash():
    """
    Tests whether ``Attachment.__hash__`` works as intended.
    """
    application = Application.precreate(202502020010)
    attachment_id = 202211010007
    clip_created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    clip_users = [
        User.precreate(202502020030),
        User.precreate(202502020031),
    ]
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
        application = application,
        clip_created_at = clip_created_at,
        clip_users = clip_users,
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
    
    vampytest.assert_instance(hash(attachment), int)


def _iter_options__eq():
    application = Application.precreate(202502020011)
    clip_created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    clip_users = [
        User.precreate(202502020032),
        User.precreate(202502020033),
    ]
    content_type = 'application/json'
    description = 'Nue'
    duration = 12.6
    flags = AttachmentFlag(12)
    height = 1000
    name = 'i miss you'
    size = 999
    temporary = True
    title = 'flandre'
    url = 'https://www.astil.dev/'
    waveform = 'kisaki'
    width = 998
    
    keyword_parameters = {
        'application': application,
        'clip_created_at': clip_created_at,
        'clip_users': clip_users,
        'content_type': content_type,
        'description': description,
        'duration': duration,
        'flags': flags,
        'height': height,
        'name': name,
        'size': size,
        'temporary': temporary,
        'title': title,
        'url': url,
        'waveform': waveform,
        'width': width,
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
            'application': Application.precreate(202502020013),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'clip_created_at': DateTime(2016, 5, 15, tzinfo = TimeZone.utc),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'clip_users': [
                User.precreate(202502020034),
                User.precreate(202502020035),
            ],
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'content_type': 'image/png',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'description': 'Remilia',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'duration': 56.6,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'flags': AttachmentFlag(3),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'height': 702,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'name': 'Slave of Scarlet',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'size': 701,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'temporary': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'title': 'remilia',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'url': 'https://orindance.party/',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'waveform': 'revenge',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'width': 7000,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__Attachment__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``Attachment.__eq__`` works as intended.
    
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
    attachment_0 = Attachment(**keyword_parameters_0)
    attachment_1 = Attachment(**keyword_parameters_1)
    
    output = attachment_0 == attachment_1
    vampytest.assert_instance(output, bool)
    return output


def test__Attachment__eq__non_partial():
    """
    Tests whether ``Attachment.__eq__`` works as intended.
    
    Case: non partial.
    """
    attachment_id = 202211010008
    name = 'vivienne'
    proxy_url = 'https://orindance.party/'
    
    
    attachment = Attachment.precreate(
        attachment_id,
        name = name,
        proxy_url = proxy_url,
    )
    
    # itself
    vampytest.assert_eq(attachment, attachment)
    
    # other type
    vampytest.assert_ne(attachment, object())
    
    # with partial
    test_attachment = Attachment(
        name = name,
    )
    
    vampytest.assert_eq(attachment, test_attachment)
