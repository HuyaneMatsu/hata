import vampytest

from ..fields import put_role_into
from ..preinstanced import TeamMemberRole


def _iter_options():
    yield TeamMemberRole.admin, False, {'role': TeamMemberRole.admin.value}
    yield TeamMemberRole.admin, True, {'role': TeamMemberRole.admin.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_role_into(input_value, defaults):
    """
    Tests whether ``put_role_into`` is working as intended.
    
    Parameters
    ----------
    input_value : ``TeamMemberRole``
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_role_into(input_value, {}, defaults)
