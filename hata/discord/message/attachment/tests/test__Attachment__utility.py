from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....application import Application
from ....user import User
from ....utils import id_to_datetime

from ..attachment import Attachment
from ..flags import AttachmentFlag

from .test__Attachment__constructor import _assert_fields_set


def test__Attachment__copy__default():
    """
    Tests whether ``Attachment.copy`` works as intended.
    
    Case: default.
    """
    application = Application.precreate(202502020014)
    clip_created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    clip_users = [
        User.precreate(202502020036),
        User.precreate(202502020037),
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
    
    attachment = Attachment(
        application = application,
        clip_created_at = clip_created_at,
        clip_users = clip_users,
        content_type = content_type,
        description = description,
        duration = duration,
        flags = flags,
        height = height,
        name = name,
        size = size,
        temporary = temporary,
        title = title,
        url = url,
        waveform = waveform,
        width = width,
    )
    copy = attachment.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(attachment, copy)
    
    vampytest.assert_eq(attachment, copy)


def test__Attachment__copy__non_partial():
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


def test__Attachment__copy_with__no_fields():
    """
    Tests whether ``Attachment.copy_with`` works as intended.
    
    Case: no fields given.
    """
    application = Application.precreate(202502020015)
    clip_created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    clip_users = [
        User.precreate(202502020038),
        User.precreate(202502020039),
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
    
    attachment = Attachment(
        application = application,
        clip_created_at = clip_created_at,
        clip_users = clip_users,
        content_type = content_type,
        description = description,
        duration = duration,
        flags = flags,
        height = height,
        name = name,
        size = size,
        temporary = temporary,
        title = title,
        url = url,
        waveform = waveform,
        width = width,
    )
    copy = attachment.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(attachment, copy)
    
    vampytest.assert_eq(attachment, copy)


def test__Attachment__copy_with__non_partial():
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


def test__Attachment__copy_with__all_fields():
    """
    Tests whether ``Attachment.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_application = Application.precreate(202502020016)
    old_clip_created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    old_clip_users = [
        User.precreate(202502020040),
        User.precreate(202502020041),
    ]
    old_content_type = 'application/json'
    old_description = 'Nue'
    old_duration = 12.6
    old_flags = AttachmentFlag(12)
    old_height = 1000
    old_name = 'i miss you'
    old_size = 999
    old_temporary = True
    old_title = 'flandre'
    old_url = 'https://www.astil.dev/'
    old_waveform = 'kisaki'
    old_width = 998
    
    new_application = Application.precreate(202502020017)
    new_clip_created_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    new_clip_users = [
        User.precreate(202502020042),
        User.precreate(202502020043),
    ]
    new_content_type = 'image/png'
    new_description = 'Remilia'
    new_duration = 69.4
    new_flags = AttachmentFlag(3)
    new_height = 702
    new_name = 'Slave of Scarlet'
    new_size = 701
    new_temporary = False
    new_title = 'remilia'
    new_url = 'https://orindance.party/'
    new_waveform = 'kisaki'
    new_width = 700
    
    attachment = Attachment(
        application = old_application,
        clip_created_at = old_clip_created_at,
        clip_users = old_clip_users,
        content_type = old_content_type,
        description = old_description,
        duration = old_duration,
        flags = old_flags,
        height = old_height,
        name = old_name,
        size = old_size,
        temporary = old_temporary,
        title = old_title,
        url = old_url,
        waveform = old_waveform,
        width = old_width,
    )
    
    copy = attachment.copy_with(
        application = new_application,
        clip_created_at = new_clip_created_at,
        clip_users = new_clip_users,
        content_type = new_content_type,
        description = new_description,
        duration = new_duration,
        flags = new_flags,
        height = new_height,
        name = new_name,
        size = new_size,
        temporary = new_temporary,
        title = new_title,
        url = new_url,
        waveform = new_waveform,
        width = new_width,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(attachment, copy)
    
    vampytest.assert_is(copy.application, new_application)
    vampytest.assert_eq(copy.clip_created_at, new_clip_created_at)
    vampytest.assert_eq(copy.clip_users, tuple(new_clip_users))
    vampytest.assert_eq(copy.content_type, new_content_type)
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_eq(copy.duration, new_duration)
    vampytest.assert_eq(copy.flags, new_flags)
    vampytest.assert_eq(copy.height, new_height)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.size, new_size)
    vampytest.assert_eq(copy.temporary, new_temporary)
    vampytest.assert_eq(copy.title, new_title)
    vampytest.assert_eq(copy.url, new_url)
    vampytest.assert_eq(copy.waveform, new_waveform)
    vampytest.assert_eq(copy.width, new_width)


def _iter_options__display_name():
    yield 'orin.txt', 'okuu', 'okuu.txt'
    yield 'orin.txt', None, 'orin.txt'
    yield None, 'okuu', 'okuu'
    yield None, None, ''


@vampytest._(vampytest.call_from(_iter_options__display_name()).returning_last())
def test__Attachment__display_name(name, title):
    """
    Tests whether ``Attachment.display_name`` works as intended.
    
    Parameters
    ----------
    name : `None | str`
        Attachment's name.
    
    title : `None | str`
        Attachment's title.
    
    Returns
    -------
    output : `str`
    """
    attachment = Attachment(name = name, title = title)
    output = attachment.display_name
    vampytest.assert_instance(output, str)
    return output


def _iter_options__content_created_at():
    attachment_id_0 = 202503050000_000000
    attachment_id_1 = 202503050001_000000
    
    date_0 = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield attachment_id_0, None, id_to_datetime(attachment_id_0)
    yield attachment_id_1, date_0, date_0


@vampytest._(vampytest.call_from(_iter_options__content_created_at()).returning_last())
def test__Attachment__content_created_at(attachment_id, clip_created_at):
    """
    Tests whether ``Attachment.content_created_at`` works as intended.
    
    Parameters
    ----------
    attachment_id : `int`
        Identifier to create the attachment_with
    
    clip_created_at : `DateTime`
        If the attachment is a clip then when the clip was created.
    
    Returns
    -------
    output : `DateTime`
    """
    attachment = Attachment.precreate(attachment_id, clip_created_at = clip_created_at)
    output = attachment.content_created_at
    vampytest.assert_instance(output, DateTime)
    return output


def _iter_options__iter_clip_users():
    clip_user_0 = User.precreate(202502020050, name = 'Koishi')
    clip_user_1 = User.precreate(202502020051, name = 'Satori')
    
    yield None, []
    yield [clip_user_0], [clip_user_0]
    yield [clip_user_0, clip_user_1], [clip_user_0, clip_user_1]


@vampytest._(vampytest.call_from(_iter_options__iter_clip_users()).returning_last())
def test__Attachment__iter_clip_users(input_value):
    """
    Tests whether ``Attachment.iter_clip_users`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<ClientUserBase>`
        Value to test with.
    
    Returns
    -------
    output : `list<User>`
    """
    attachment = Attachment(clip_users = input_value)
    return [*attachment.iter_clip_users()]
