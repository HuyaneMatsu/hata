import vampytest

from ..preinstanced import Status, SessionPlatformType
from ..status_by_platform import StatusByPlatform

from .test__StatusByPlatform__constructor import _assert_fields_set


def test__StatusByPlatform__copy():
    """
    Tests whether ``StatusByPlatform.copy`` works as intended.
    """
    desktop = Status.invisible
    embedded = Status.online
    mobile = Status.idle
    web = Status.dnd
    
    status_by_platform = StatusByPlatform(
        desktop = desktop,
        embedded = embedded,
        mobile = mobile,
        web = web,
    )
    
    copy = status_by_platform.copy()
    _assert_fields_set(copy)
    
    vampytest.assert_eq(copy, status_by_platform)


def test__StatusByPlatform__copy_with__no_fields():
    """
    Tests whether ``StatusByPlatform.copy_with`` works as intended.
    
    Case: no fields given.
    """
    desktop = Status.invisible
    embedded = Status.online
    mobile = Status.idle
    web = Status.dnd
    
    status_by_platform = StatusByPlatform(
        desktop = desktop,
        embedded = embedded,
        mobile = mobile,
        web = web,
    )
    
    copy = status_by_platform.copy_with()
    _assert_fields_set(copy)
    
    vampytest.assert_eq(copy, status_by_platform)


def test__StatusByPlatform__copy_with__all_fields():
    """
    Tests whether ``StatusByPlatform.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_desktop = Status.invisible
    old_embedded = Status.online
    old_mobile = Status.idle
    old_web = Status.dnd
    
    new_desktop = Status.online
    new_embedded = Status.dnd
    new_mobile = Status.invisible
    new_web = Status.idle
    
    status_by_platform = StatusByPlatform(
        desktop = old_desktop,
        embedded = old_embedded,
        mobile = old_mobile,
        web = old_web,
    )
    
    copy = status_by_platform.copy_with(
        desktop = new_desktop,
        embedded = new_embedded,
        mobile = new_mobile,
        web = new_web,
    )
    _assert_fields_set(copy)
    
    vampytest.assert_ne(copy, status_by_platform)
    
    vampytest.assert_is(copy.desktop, new_desktop)
    vampytest.assert_is(copy.embedded, new_embedded)
    vampytest.assert_is(copy.mobile, new_mobile)
    vampytest.assert_is(copy.web, new_web)


def test__StatusByPlatform__iter_status_by_platform():
    """
    Tests whether ``StatusByPlatform.iter_status_by_platform`` works as intended.
    """
    desktop = Status.invisible
    embedded = Status.online
    mobile = Status.idle
    web = Status.dnd
    
    status_by_platform = StatusByPlatform(
        desktop = desktop,
        embedded = embedded,
        mobile = mobile,
        web = web,
    )
    
    vampytest.assert_eq(
        [*status_by_platform.iter_status_by_platform()],
        [
            (SessionPlatformType.desktop, desktop),
            (SessionPlatformType.embedded, embedded),
            (SessionPlatformType.mobile, mobile),
            (SessionPlatformType.web, web),
        ],
    )
