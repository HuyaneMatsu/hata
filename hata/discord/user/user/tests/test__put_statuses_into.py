import vampytest

from ..fields import put_statuses_into


def test__put_statuses_into():
    """
    Tests whether ``put_statuses_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        ({}, False, {'client_status': {}}),
        ({}, True, {'client_status': {}}),
        ({'mobile': 'online'}, False, {'client_status': {'mobile': 'online'}}),
        ({'mobile': 'online'}, True, {'client_status': {'mobile': 'online'}}),
    ):
        data = put_statuses_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
