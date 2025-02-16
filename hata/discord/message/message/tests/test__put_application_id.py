import vampytest

from ..fields import put_application_id


def _iter_options():
    application_id = 202304280051
    webhook_id = 202304280052
    
    yield (
        0,
        {},
        False,
        {},
    )
    yield (
        0,
        {},
        True,
        {
            'application_id': None,
        },
    )
    yield (
        0,
        {
            'webhook_id': None,
        },
        False,
        {
            'webhook_id': None,
        },
    )
    yield (
        0,
        {
            'webhook_id': None,
        },
        True,
        {
            'webhook_id': None,
            'application_id': None,
        },
    )
    yield (
        0,
        {
            'webhook_id': str(webhook_id),
        },
        False,
        {
            'webhook_id': str(webhook_id),
        },
    )
    yield (
        0,
        {
            'webhook_id': str(webhook_id),
        },
        True,
        {
            'webhook_id': str(webhook_id),
            'application_id': None,
        },
    )
    yield (
        application_id,
        {},
        False,
        {
            'application_id': str(application_id),
            'webhook_id': str(application_id),
        },
    )
    yield (
        application_id,
        {},
        True,
        {
            'application_id': str(application_id),
            'webhook_id': str(application_id),
        },
    )
    yield (
        application_id,
        {
            'webhook_id': None,
        },
        False,
        {
            'application_id': str(application_id),
            'webhook_id': str(application_id),
        },
    )
    yield (
        application_id,
        {
            'webhook_id': None,
        },
        True,
        {
            'application_id': str(application_id),
            'webhook_id': str(application_id),
        },
    )
    yield (
        application_id,
        {
            'webhook_id': str(webhook_id),
        },
        False,
        {
            'application_id': str(application_id),
            'webhook_id': str(webhook_id),
        },
    )
    yield (
        application_id,
        {
            'webhook_id': str(webhook_id),
        },
        True,
        {
            'application_id': str(application_id),
            'webhook_id': str(webhook_id),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_application_id(input_value, data, defaults):
    """
    Tests whether ``put_application_id`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        The value to serialise.
    data : `dict<str, object>`
        Data to extend.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_application_id(input_value, data.copy(), defaults)
