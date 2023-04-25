import vampytest

from ..attachment import Attachment

from .test__Attachment__constructor import _assert_fields_set


def test__Attachment__copy__0():
    """
    Tests whether ``Attachment.copy`` works as intended.
    
    Case: default.
    """
    content_type = 'application/json'
    description = 'Nue'
    duration = 12.6
    height = 1000
    name = 'i miss you'
    size = 999
    temporary = True
    url = 'https://www.astil.dev/'
    waveform = 'kisaki'
    width = 998
    
    attachment = Attachment(
        content_type = content_type,
        description = description,
        duration = duration,
        height = height,
        name = name,
        size = size,
        temporary = temporary,
        url = url,
        waveform = waveform,
        width = width,
    )
    copy = attachment.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(attachment, copy)
    
    vampytest.assert_eq(attachment, copy)


def test__Attachment__copy__1():
    """
    Tests whether ``Attachment.copy`` works as intended.
    
    Case: non-partial.
    """
    attachment_id = 202211010002
    proxy_url = 'https://orindance.party/'
    
    attachment = Attachment.precreate(
        attachment_id,
        proxy_url = proxy_url,
    )
    
    copy = attachment.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(attachment, copy)
    
    vampytest.assert_eq(copy.id, 0)
    vampytest.assert_is(copy.proxy_url, None)


def test__Attachment__copy_with__0():
    """
    Tests whether ``Attachment.copy_with`` works as intended.
    
    Case: no fields given.
    """
    content_type = 'application/json'
    description = 'Nue'
    duration = 12.6
    height = 1000
    name = 'i miss you'
    size = 999
    temporary = True
    url = 'https://www.astil.dev/'
    waveform = 'kisaki'
    width = 998
    
    attachment = Attachment(
        content_type = content_type,
        description = description,
        duration = duration,
        height = height,
        name = name,
        size = size,
        temporary = temporary,
        url = url,
        waveform = waveform,
        width = width,
    )
    copy = attachment.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(attachment, copy)
    
    vampytest.assert_eq(attachment, copy)


def test__Attachment__copy_with__1():
    """
    Tests whether ``Attachment.copy_with`` works as intended.
    
    Case: non-partial.
    """
    attachment_id = 202211010003
    proxy_url = 'https://orindance.party/'
    
    attachment = Attachment.precreate(
        attachment_id,
        proxy_url = proxy_url,
    )
    
    copy = attachment.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(attachment, copy)
    
    vampytest.assert_eq(copy.id, 0)
    vampytest.assert_is(copy.proxy_url, None)


def test__Attachment__copy_with__2():
    """
    Tests whether ``Attachment.copy_with`` works as intended.
    
    Case: non-partial.
    """
    old_content_type = 'application/json'
    old_description = 'Nue'
    old_duration = 12.6
    old_height = 1000
    old_name = 'i miss you'
    old_size = 999
    old_temporary = True
    old_url = 'https://www.astil.dev/'
    old_waveform = 'kisaki'
    old_width = 998
    
    new_content_type = 'image/png'
    new_description = 'Remilia'
    new_duration = 69.4
    new_height = 702
    new_name = 'Slave of Scarlet'
    new_size = 701
    new_temporary = False
    new_url = 'https://orindance.party/'
    new_waveform = 'kisaki'
    new_width = 700
    
    attachment = Attachment(
        content_type = old_content_type,
        description = old_description,
        duration = old_duration,
        height = old_height,
        name = old_name,
        size = old_size,
        temporary = old_temporary,
        url = old_url,
        waveform = old_waveform,
        width = old_width,
    )
    
    copy = attachment.copy_with(
        content_type = new_content_type,
        description = new_description,
        duration = new_duration,
        height = new_height,
        name = new_name,
        size = new_size,
        temporary = new_temporary,
        url = new_url,
        waveform = new_waveform,
        width = new_width,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(attachment, copy)

    vampytest.assert_eq(copy.content_type, new_content_type)
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_eq(copy.duration, new_duration)
    vampytest.assert_eq(copy.height, new_height)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.size, new_size)
    vampytest.assert_eq(copy.temporary, new_temporary)
    vampytest.assert_eq(copy.url, new_url)
    vampytest.assert_eq(copy.waveform, new_waveform)
    vampytest.assert_eq(copy.width, new_width)
