import vampytest

from ..fields import parse_state
from ..preinstanced import TeamMembershipState


def test__parse_state():
    """
    Tests whether `parse_state` works as intended.
    """
    for input_value, expected_output in (
        ({}, TeamMembershipState.none),
        ({'membership_state': TeamMembershipState.invited.value}, TeamMembershipState.invited),
    ):
        output = parse_state(input_value)
        vampytest.assert_eq(output, expected_output)
