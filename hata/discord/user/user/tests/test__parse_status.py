import vampytest

from ..fields import parse_status
from ..preinstanced import Status


def test__parse_status():
    """
    Tests whether ``parse_status`` works as intended.
    """
    for input_data, expected_output in (
        ({}, Status.offline),
        ({'status': Status.online.value}, Status.online),
    ):
        output = parse_status(input_data)
        vampytest.assert_eq(output, expected_output)
