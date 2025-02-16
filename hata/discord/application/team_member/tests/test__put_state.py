import vampytest

from ..fields import put_state
from ..preinstanced import TeamMembershipState


def test__put_state():
    """
    Tests whether ``put_state`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (TeamMembershipState.invited, True, {'membership_state': TeamMembershipState.invited.value}),
    ):
        data = put_state(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
