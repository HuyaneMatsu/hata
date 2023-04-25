import vampytest

from ..attachment import Attachment


def _assert_fields_set(attachment):
    """
    Tests whether all attributes are set of the given attachment.
    
    Parameters
    ----------
    attachment : ``Attachment``
        The attachment to check.
    """
    vampytest.assert_instance(attachment, Attachment)
    vampytest.assert_instance(attachment.content_type, str, nullable = True)
    vampytest.assert_instance(attachment.description, str, nullable = True)
    vampytest.assert_instance(attachment.duration, float)
    vampytest.assert_instance(attachment.height, int)
    vampytest.assert_instance(attachment.id, int)
    vampytest.assert_instance(attachment.name, str)
    vampytest.assert_instance(attachment.proxy_url, str, nullable = True)
    vampytest.assert_instance(attachment.size, int)
    vampytest.assert_instance(attachment.temporary, bool)
    vampytest.assert_instance(attachment.url, str)
    vampytest.assert_instance(attachment.waveform, str, nullable = True)
    vampytest.assert_instance(attachment.width, int)


def test__Attachment__new__0():
    """
    Tests whether ``Attachment.__new__`` works as intended.
    
    Case: No fields given.
    """
    attachment = Attachment()
    _assert_fields_set(attachment)


def test__Attachment__new__1():
    """
    Tests whether ``Attachment.__new__`` works as intended.
    
    Case: All fields given.
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
    _assert_fields_set(attachment)
    
    vampytest.assert_eq(attachment.content_type, content_type)
    vampytest.assert_eq(attachment.description, description)
    vampytest.assert_eq(attachment.duration, duration)
    vampytest.assert_eq(attachment.height, height)
    vampytest.assert_eq(attachment.name, name)
    vampytest.assert_eq(attachment.size, size)
    vampytest.assert_eq(attachment.temporary, temporary)
    vampytest.assert_eq(attachment.url, url)
    vampytest.assert_eq(attachment.waveform, waveform)
    vampytest.assert_eq(attachment.width, width)


def test__Attachment__precreate__0():
    """
    Tests whether ``Attachment.precreate`` works as intended.
    
    Case: No fields given.
    """
    attachment_id = 202211010000
    
    attachment = Attachment.precreate(attachment_id)
    _assert_fields_set(attachment)
    
    vampytest.assert_eq(attachment.id, attachment_id)


def test__Attachment__precreate__1():
    """
    Tests whether ``Attachment.precreate`` works as intended.
    
    Case: No fields given.
    """
    attachment_id = 202211010001
    
    content_type = 'application/json'
    description = 'Nue'
    duration = 12.6
    height = 1000
    name = 'i miss you'
    proxy_url = 'https://orindance.party/'
    size = 999
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
    _assert_fields_set(attachment)
    
    vampytest.assert_eq(attachment.id, attachment_id)
    vampytest.assert_eq(attachment.proxy_url, proxy_url)

    vampytest.assert_eq(attachment.content_type, content_type)
    vampytest.assert_eq(attachment.description, description)
    vampytest.assert_eq(attachment.duration, duration)
    vampytest.assert_eq(attachment.height, height)
    vampytest.assert_eq(attachment.name, name)
    vampytest.assert_eq(attachment.size, size)
    vampytest.assert_eq(attachment.temporary, temporary)
    vampytest.assert_eq(attachment.url, url)
    vampytest.assert_eq(attachment.waveform, waveform)
    vampytest.assert_eq(attachment.width, width)
