import vampytest

from ..preinstanced import SessionPlatformType, Status
from ..status_by_platform import StatusByPlatform


def test__StatusByPlatform__repr():
    """
    Tests whether ``StatusByPlatform.__repr__`` works as intended.
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
    
    output = repr(status_by_platform)
    vampytest.assert_instance(output, str)


def test__StatusByPlatform__hash():
    """
    Tests whether ``StatusByPlatform.__hash__`` works as intended.
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
    
    output = hash(status_by_platform)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    desktop = Status.invisible
    embedded = Status.online
    mobile = Status.idle
    web = Status.dnd
    
    keyword_parameters = {
        'desktop' : desktop,
        'embedded' : embedded,
        'mobile' : mobile,
        'web' :  web,
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
            'desktop': Status.offline,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'embedded': Status.offline,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'mobile': Status.offline,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'web': Status.offline,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__StatusByPlatform__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``StatusByPlatform.__eq__`` works as intended.
    
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
    status_by_platform_0 = StatusByPlatform(**keyword_parameters_0)
    status_by_platform_1 = StatusByPlatform(**keyword_parameters_1)
    
    output = status_by_platform_0 == status_by_platform_1
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__getitem():
    desktop = Status.invisible
    embedded = Status.online
    mobile = Status.idle
    web = Status.dnd
    
    keyword_parameters = {
        'desktop' : desktop,
        'embedded' : embedded,
        'mobile' : mobile,
        'web' :  web,
    }
    
    yield (
        keyword_parameters,
        SessionPlatformType.desktop,
        desktop,
    )
    
    yield (
        keyword_parameters,
        SessionPlatformType.embedded,
        embedded,
    )
    
    yield (
        keyword_parameters,
        SessionPlatformType.mobile,
        mobile,
    )
    
    yield (
        keyword_parameters,
        SessionPlatformType.web,
        web,
    )


@vampytest._(vampytest.call_from(_iter_options__getitem()).returning_last())
def test__StatusByPlatform__getitem(keyword_parameters, platform):
    """
    Tests whether ``StatusByPlatform.__getitem__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    platform : ``SessionPlatformType``
        Platform to get status for.
    
    Returns
    -------
    output : ``Status``
    """
    status_by_platform = StatusByPlatform(**keyword_parameters)
    output = status_by_platform[platform]
    vampytest.assert_instance(output, Status)
    return output
