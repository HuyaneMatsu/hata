import vampytest

from ..fields import put_target_type_into
from ..preinstanced import ApplicationCommandTargetType


def _iter_options():
    yield (
        ApplicationCommandTargetType.user,
        False,
        {'type': ApplicationCommandTargetType.user.value},
    )

    yield (
        ApplicationCommandTargetType.user,
        True,
        {'type': ApplicationCommandTargetType.user.value},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_target_type_into(input_value, defaults):
    """
    Tests whether ``put_target_type_into`` works as intended.
    
    Parameters
    ----------
    input_value : ``ApplicationCommandTargetType``
        The value to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_target_type_into(input_value, {}, defaults)
