import vampytest

from ....application import ApplicationIntegrationType

from ..fields import put_integration_types


def _iter_options():
    yield None, False, {'integration_types': None}
    yield None, True, {'integration_types': None}
    yield (
        (ApplicationIntegrationType.user_install, ),
        False,
        {'integration_types': [ApplicationIntegrationType.user_install.value]},
    )
    yield (
        (ApplicationIntegrationType.user_install, ),
        True,
        {'integration_types': [ApplicationIntegrationType.user_install.value]},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_integration_types(input_value, defaults):
    """
    Tests whether ``put_integration_types`` is working as intended.
    
    Parameters
    ----------
    input_value : `none | tuple<ApplicationIntegrationType>`
        Value to serialize.
    defaults : `bool`
        Whether fields with their default value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_integration_types(input_value, {}, defaults)
