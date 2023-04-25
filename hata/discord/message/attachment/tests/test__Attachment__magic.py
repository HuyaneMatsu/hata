import vampytest

from ..attachment import Attachment


def test__Attachment__repr():
    """
    Tests whether ``Attachment.__repr__`` works as intended.
    """
    attachment_id = 202211010006
    content_type = 'application/json'
    description = 'Nue'
    duration = 12.6
    height = 1000
    name = 'i miss you'
    size = 999
    proxy_url = 'https://orindance.party/'
    temporary = True
    url = 'https://www.astil.dev/'
    width = 998
    
    attachment = Attachment.precreate(
        attachment_id,
        content_type = content_type,
        description = description,
        duration = duration,
        height = height,
        name = name,
        proxy_url = proxy_url,
        size = size,
        temporary = temporary,
        url = url,
        width = width,
    )
    
    vampytest.assert_instance(repr(attachment), str)


def test__Attachment__hash():
    """
    Tests whether ``Attachment.__hash__`` works as intended.
    """
    attachment_id = 202211010007
    content_type = 'application/json'
    description = 'Nue'
    duration = 12.6
    height = 1000
    name = 'i miss you'
    size = 999
    proxy_url = 'https://orindance.party/'
    temporary = True
    url = 'https://www.astil.dev/'
    waveform = 'kisaki'
    width = 998
    
    attachment = Attachment.precreate(
        attachment_id,
        content_type = content_type,
        description = description,
        duration = duration,
        height = height,
        name = name,
        proxy_url = proxy_url,
        size = size,
        temporary = temporary,
        url = url,
        waveform = waveform,
        width = width,
    )
    
    vampytest.assert_instance(hash(attachment), int)


def test__Attachment__eq():
    """
    Tests whether ``Attachment.__eq__`` works as intended.
    """
    attachment_id = 202211010008
    content_type = 'application/json'
    description = 'Nue'
    duration = 12.6
    height = 1000
    name = 'i miss you'
    size = 999
    proxy_url = 'https://orindance.party/'
    temporary = True
    url = 'https://www.astil.dev/'
    waveform = 'kisaki'
    width = 998
    
    keyword_parameters = {
        'content_type': content_type,
        'description': description,
        'duration': duration,
        'height': height,
        'name': name,
        'size': size,
        'temporary': temporary,
        'url': url,
        'waveform': waveform,
        'width': width,
    }
    
    attachment = Attachment.precreate(
        attachment_id,
        proxy_url = proxy_url,
        **keyword_parameters,
    )
    
    vampytest.assert_eq(attachment, attachment)
    vampytest.assert_ne(attachment, object())
    
    # Since we do a shortcut check, we create the same attachment twice
    test_attachment = Attachment.precreate(
        attachment_id,
        proxy_url = proxy_url,
        **keyword_parameters,
    )
    vampytest.assert_eq(attachment, test_attachment)
    
    test_attachment = Attachment(**keyword_parameters)
    vampytest.assert_eq(attachment, test_attachment)
    
    for field_name, field_value in (
        ('content_type', 'image/png'),
        ('description', 'Remilia'),
        ('duration', 56.6),
        ('height', 702),
        ('name', 'Slave of Scarlet'),
        ('size', 701),
        ('temporary', False),
        ('url', 'https://orindance.party/'),
        ('waveform', 'revenge'),
        ('width', 7000),
    ):
        test_attachment = Attachment(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(attachment, test_attachment)
