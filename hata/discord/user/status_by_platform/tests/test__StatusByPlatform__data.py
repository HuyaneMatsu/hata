import vampytest

from ..preinstanced import Status
from ..status_by_platform import StatusByPlatform

from .test__StatusByPlatform__constructor import _assert_fields_set


def test__StatusByPlatform__from_data():
    """
    Tests whether ``StatusByPlatform.from_data`` works as intended.
    """
    desktop = Status.invisible
    embedded = Status.online
    mobile = Status.idle
    web = Status.dnd
    
    data = {
        'desktop': desktop.value,
        'embedded': embedded.value,
        'mobile': mobile.value,
        'web': web.value,
    }
    
    status_by_platform = StatusByPlatform.from_data(data)
    _assert_fields_set(status_by_platform)
    
    vampytest.assert_is(status_by_platform.desktop, desktop)
    vampytest.assert_is(status_by_platform.embedded, embedded)
    vampytest.assert_is(status_by_platform.mobile, mobile)
    vampytest.assert_is(status_by_platform.web, web)


def test__StatusByPlatform__to_data():
    """
    Tests whether ``StatusByPlatform.to_data`` works as intended.
    
    Case: include defaults.
    """
    desktop = Status.invisible
    embedded = Status.online
    mobile = Status.idle
    web = Status.dnd
    
    expected_output = {
        'desktop': desktop.value,
        'embedded': embedded.value,
        'mobile': mobile.value,
        'web': web.value,
    }
    
    status_by_platform = StatusByPlatform(
        desktop = desktop,
        embedded = embedded,
        mobile = mobile,
        web = web,
    )
    output = status_by_platform.to_data(defaults = True)
    
    vampytest.assert_eq(
        output,
        expected_output,
    )
