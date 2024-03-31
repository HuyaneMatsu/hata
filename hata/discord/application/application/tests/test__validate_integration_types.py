import vampytest

from ..fields import validate_integration_types
from ..preinstanced import ApplicationIntegrationType


def _iter_options__passing():
    yield None, None
    yield [], None
    yield [ApplicationIntegrationType.user_install], (ApplicationIntegrationType.user_install, )
    yield [ApplicationIntegrationType.user_install.value], (ApplicationIntegrationType.user_install, )
    yield (
        [ApplicationIntegrationType.user_install, ApplicationIntegrationType.guild_install],
        (ApplicationIntegrationType.guild_install, ApplicationIntegrationType.user_install),
    )


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_integration_types(input_value):
    """
    Tests whether `validate_integration_types` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | tuple<ApplicationIntegrationType>`
    
    Raises
    ------
    TypeError
    """
    return validate_integration_types(input_value)
