import vampytest

from ..fields import put_owner
from ..preinstanced import EntitlementOwnerType


def _iter_options():
    owner_id = 202310030002

    yield (
        (EntitlementOwnerType.user, owner_id),
        False,
        {
            'owner_id': str(owner_id),
            'owner_type': EntitlementOwnerType.user.value,
        }
    )

    yield (
        (EntitlementOwnerType.user, owner_id),
        True,
        {
            'owner_id': str(owner_id),
            'owner_type': EntitlementOwnerType.user.value,
        }
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_owner(input_value, defaults):
    """
    Tests whether ``put_owner`` works as intended.
    
    Parameters
    ----------
    input_value : ``(EntitlementOwnerType, int)``
        The value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_owner(input_value, {}, defaults)
