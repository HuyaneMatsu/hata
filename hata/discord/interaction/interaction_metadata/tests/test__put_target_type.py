import vampytest

from ....application_command import ApplicationCommandTargetType

from ..fields import put_target_type


def _iter_options():
    yield (
        ApplicationCommandTargetType.none,
        False,
        {'type': ApplicationCommandTargetType.none.value},
    )

    yield (
        ApplicationCommandTargetType.none,
        True,
        {'type': ApplicationCommandTargetType.none.value},
    )
    
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
def test__put_target_type(input_value, defaults):
    """
    Tests whether ``put_target_type`` works as intended.
    
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
    return put_target_type(input_value, {}, defaults)
