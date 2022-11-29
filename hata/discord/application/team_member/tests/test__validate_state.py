import vampytest

from ..fields import validate_state
from ..preinstanced import TeamMembershipState


def test__validate_state__0():
    """
    Tests whether ``validate_state`` works as intended.
    """
    for input_value, expected_output in (
        (TeamMembershipState.invited, TeamMembershipState.invited.value),
        (TeamMembershipState.invited.value, TeamMembershipState.invited.value),
    ):
        output = validate_state(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_state__1():
    """
    Tests whether `validate_state` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_state(input_value)
