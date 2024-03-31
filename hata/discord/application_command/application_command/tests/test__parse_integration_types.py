import vampytest

from ....application import ApplicationIntegrationType

from ..fields import parse_integration_types


def _iter_options():
    yield {}, None
    yield {'integration_types': None}, None
    yield {'integration_types': []}, None
    yield (
        {'integration_types': [ApplicationIntegrationType.user_install.value]},
        (ApplicationIntegrationType.user_install,),
    )
    yield (
        {
            'integration_types': [
                ApplicationIntegrationType.user_install.value,
                ApplicationIntegrationType.guild_install.value
            ],
        },
        (ApplicationIntegrationType.guild_install, ApplicationIntegrationType.user_install,),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_integration_types(input_data):
    """
    Tests whether ``parse_integration_types`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<ApplicationIntegrationType>`
    """
    return parse_integration_types(input_data)
