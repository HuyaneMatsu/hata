import vampytest

from ....application import ApplicationIntegrationType

from ..fields import parse_authorizer_user_ids


def _iter_options():
    user_id_0 = 202407160082
    user_id_1 = 202407160083
    
    yield {}, None
    yield {'authorizing_integration_owners': None}, None 
    yield {'authorizing_integration_owners': {}}, None
    
    yield (
        {
            'authorizing_integration_owners': {
                str(ApplicationIntegrationType.user_install.value): str(user_id_0),
                str(ApplicationIntegrationType.guild_install.value): str(user_id_1),
            }
        },
        {
            ApplicationIntegrationType.user_install: user_id_0,
            ApplicationIntegrationType.guild_install: user_id_1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_authorizer_user_ids(input_data):
    """
    Tests whether ``parse_authorizer_user_ids`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | dict<ApplicationIntegrationType, int>`
    """
    return parse_authorizer_user_ids(input_data)
