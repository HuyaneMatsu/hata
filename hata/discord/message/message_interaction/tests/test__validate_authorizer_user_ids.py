import vampytest

from ....application import ApplicationIntegrationType
from ....user import User

from ..fields import validate_authorizer_user_ids


def _iter_options__passing():
    yield None, None
    yield {}, None
    
    user_id_0 = 202403270005
    user_id_1 = 202403270006
    
    yield (
        {
            ApplicationIntegrationType.user_install: user_id_0,
            ApplicationIntegrationType.guild_install: user_id_1,
        },
        {
            ApplicationIntegrationType.user_install: user_id_0,
            ApplicationIntegrationType.guild_install: user_id_1,
        },
    )
    
    yield (
        {
            ApplicationIntegrationType.user_install.value: user_id_0,
        },
        {
            ApplicationIntegrationType.user_install: user_id_0,
        },
    )

    yield (
        {
            ApplicationIntegrationType.user_install: User.precreate(user_id_0),
        },
        {
            ApplicationIntegrationType.user_install: user_id_0,
        },
    )


def _iter_options__type_error():
    user_id_0 = 202403270004
    yield object()
    
    yield {2.6: user_id_0}
    yield {ApplicationIntegrationType.user_install: 2.6}


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_authorizer_user_ids(input_value):
    """
    Tests whether ``validate_authorizer_user_ids`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | dict<ApplicationIntegrationType, int>`
    
    Raises
    ------
    TypeError
    """
    return validate_authorizer_user_ids(input_value)
