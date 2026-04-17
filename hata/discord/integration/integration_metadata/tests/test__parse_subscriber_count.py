import vampytest

from ..constants import SUBSCRIBER_COUNT_DEFAULT
from ..fields import parse_subscriber_count


def test__parse_subscriber_count():
    """
    Tests whether ``parse_subscriber_count`` works as intended.
    """
    for input_data, expected_output in (
        ({}, SUBSCRIBER_COUNT_DEFAULT),
        ({'subscriber_count': None}, SUBSCRIBER_COUNT_DEFAULT),
        ({'subscriber_count': 1}, 1),
    ):
        output = parse_subscriber_count(input_data)
        vampytest.assert_eq(output, expected_output)
