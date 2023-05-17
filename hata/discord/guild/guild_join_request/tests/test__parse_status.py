import vampytest

from ..fields import parse_status
from ..preinstanced import GuildJoinRequestStatus


def test__parse_status():
    """
    Tests whether ``parse_status`` works as intended.
    """
    for input_data, expected_output in (
        ({}, GuildJoinRequestStatus.started),
        ({'application_status': GuildJoinRequestStatus.pending.value}, GuildJoinRequestStatus.pending),
    ):
        output = parse_status(input_data)
        vampytest.assert_eq(output, expected_output)
