import vampytest

from ..fields import put_owner_type
from ..preinstanced import EntitlementOwnerType


def _iter_options():
    yield EntitlementOwnerType.user, False, {'owner_type': EntitlementOwnerType.user.value}
    yield EntitlementOwnerType.user, True, {'owner_type': EntitlementOwnerType.user.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_owner_type(input_value, defaults):
    """
    Tests whether ``put_owner_type`` is working as intended.
    
    Parameters
    ----------
    input_value : ``EntitlementOwnerType``
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_owner_type(input_value, {}, defaults)
