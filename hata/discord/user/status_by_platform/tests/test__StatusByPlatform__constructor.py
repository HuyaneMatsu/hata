import vampytest

from ..preinstanced import Status
from ..status_by_platform import StatusByPlatform


def _assert_fields_set(status_by_platform):
    """
    Asserts whether every fields are set of the given instance.
    
    Parameters
    ----------
    status_by_platform : ``StatusByPlatform``
        The instance to check.
    """
    vampytest.assert_instance(status_by_platform, StatusByPlatform)
    vampytest.assert_instance(status_by_platform.desktop, Status)
    vampytest.assert_instance(status_by_platform.embedded, Status)
    vampytest.assert_instance(status_by_platform.mobile, Status)
    vampytest.assert_instance(status_by_platform.vr, Status)
    vampytest.assert_instance(status_by_platform.web, Status)


def test__StatusByPlatform__new__no_fields():
    """
    Tests whether ``StatusByPlatform.__new__`` works as intended.
    
    Case: no fields given.
    """
    status_by_platform = StatusByPlatform()
    _assert_fields_set(status_by_platform)


def test__StatusByPlatform__new__all_fields():
    """
    Tests whether ``StatusByPlatform.__new__`` works as intended.
    
    Case: all fields given.
    """
    desktop = Status.invisible
    embedded = Status.online
    mobile = Status.idle
    vr = Status.dnd
    web = Status.dnd
    
    status_by_platform = StatusByPlatform(
        desktop = desktop,
        embedded = embedded,
        mobile = mobile,
        vr = vr,
        web = web,
    )
    _assert_fields_set(status_by_platform)
    
    vampytest.assert_is(status_by_platform.desktop, desktop)
    vampytest.assert_is(status_by_platform.embedded, embedded)
    vampytest.assert_is(status_by_platform.mobile, mobile)
    vampytest.assert_is(status_by_platform.vr, vr)
    vampytest.assert_is(status_by_platform.web, web)
