import vampytest

from ..fields import put_state_into
from ..preinstanced import TeamMembershipState


def test__put_state_into():
    """
    Tests whether ``put_state_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (TeamMembershipState.invited, True, {'membership_state': TeamMembershipState.invited.value}),
    ):
        data = put_state_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
