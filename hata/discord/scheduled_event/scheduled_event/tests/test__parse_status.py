import vampytest

from ..fields import parse_status
from ..preinstanced import ScheduledEventStatus


def test__parse_status():
    """
    Tests whether ``parse_status`` works as intended.
    """
    for input_data, expected_output in (
        ({}, ScheduledEventStatus.none),
        ({'status': ScheduledEventStatus.active.value}, ScheduledEventStatus.active),
    ):
        output = parse_status(input_data)
        vampytest.assert_eq(output, expected_output)
