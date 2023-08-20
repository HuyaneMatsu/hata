import vampytest

from ..fields import put_target_type_into
from ..preinstanced import InviteTargetType


def _iter_options():
    yield (
        InviteTargetType.none,
        False,
        {},
    )

    yield (
        InviteTargetType.none,
        True,
        {},
    )
    
    yield (
        InviteTargetType.stream,
        False,
        {'target_type': InviteTargetType.stream.value},
    )

    yield (
        InviteTargetType.stream,
        True,
        {'target_type': InviteTargetType.stream.value},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_target_type_into(input_value, defaults):
    """
    Tests whether ``put_target_type_into`` works as intended.
    
    Parameters
    ----------
    input_value : ``InviteTargetType``
        The value to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_target_type_into(input_value, {}, defaults)
