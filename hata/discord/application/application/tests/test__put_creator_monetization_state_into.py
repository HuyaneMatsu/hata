import vampytest

from ..fields import put_creator_monetization_state_into
from ..preinstanced import ApplicationMonetizationState


def _iter_options():
    yield (
        ApplicationMonetizationState.disabled,
        False,
        {'creator_monetization_state': ApplicationMonetizationState.disabled.value},
    )
    yield (
        ApplicationMonetizationState.disabled,
        True,
        {'creator_monetization_state': ApplicationMonetizationState.disabled.value},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_creator_monetization_state_into(input_value, defaults):
    """
    Tests whether ``put_creator_monetization_state_into`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ApplicationMonetizationState``
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_creator_monetization_state_into(input_value, {}, defaults)
