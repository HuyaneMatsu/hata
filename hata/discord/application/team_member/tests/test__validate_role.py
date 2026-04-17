import vampytest

from ..fields import validate_role
from ..preinstanced import TeamMemberRole


def _iter_options():
    yield None, TeamMemberRole.none
    yield TeamMemberRole.admin, TeamMemberRole.admin
    yield TeamMemberRole.admin.value, TeamMemberRole.admin


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_role__passing(input_value):
    """
    Tests whether ``validate_role`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``TeamMemberRole``
    """
    output = validate_role(input_value)
    vampytest.assert_instance(output, TeamMemberRole)
    return output


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
@vampytest.call_with(12)
def test__validate_role__type_error(input_value):
    """
    Tests whether ``validate_role`` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Input value where we are expecting `TypeError`.
    
    Raises
    ------
    TypeError
    """
    validate_role(input_value)
