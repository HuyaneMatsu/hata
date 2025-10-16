import vampytest

from ....permission import Permission

from ..fields import put_application_permissions


def _iter_options():
    yield (
        Permission(),
        False,
        {
            'app_permissions': '0',
        },
    )
    
    yield (
        Permission(),
        True,
        {
            'app_permissions': '0',
        },
    )
    
    yield (
        Permission(1),
        False,
        {
            'app_permissions': '1',
        },
    )
    
    yield (
        Permission(1),
        True,
        {
            'app_permissions': '1',
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_application_permissions(input_value, defaults):
    """
    Tests whether ``put_application_permissions`` is working as intended.
    
    Parameters
    ----------
    input_value : ``Permission``
        Value to serialize.
    
    defaults : `bool`
        Whether fields as their defaults should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_application_permissions(input_value, {}, defaults)
