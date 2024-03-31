import vampytest

from ....application import ApplicationIntegrationType

from ..fields import put_authorizer_user_ids_into


def _iter_options():
    user_id_0 = 202403270002
    user_id_1 = 202403270003
    
    yield None, False, {'authorizing_integration_owners': {}}
    yield None, True, {'authorizing_integration_owners': {}}
    
    yield (
        {
            ApplicationIntegrationType.user_install: user_id_0,
            ApplicationIntegrationType.guild_install: user_id_1,
        },
        False,
        {
            'authorizing_integration_owners': {
                str(ApplicationIntegrationType.user_install.value): str(user_id_0),
                str(ApplicationIntegrationType.guild_install.value): str(user_id_1),
            }
        },
    )
    
    yield (
        {
            ApplicationIntegrationType.user_install: user_id_0,
            ApplicationIntegrationType.guild_install: user_id_1,
        },
        True,
        {
            'authorizing_integration_owners': {
                str(ApplicationIntegrationType.user_install.value): str(user_id_0),
                str(ApplicationIntegrationType.guild_install.value): str(user_id_1),
            }
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_authorizer_user_ids_into(input_value, defaults):
    """
    Tests whether ``put_authorizer_user_ids_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | dict<ApplicationIntegrationType, int>`
        Value to serialize.
    defaults : `bool`
        Whether values as their defaults should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_authorizer_user_ids_into(input_value, {}, defaults)
