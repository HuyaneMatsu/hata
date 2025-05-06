import vampytest

from ..fields import put_statuses


def test__put_statuses():
    """
    Tests whether ``put_statuses`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {'client_status': {}}),
        (None, True, {'client_status': {}}),
        ({'mobile': 'online'}, False, {'client_status': {'mobile': 'online'}}),
        ({'mobile': 'online'}, True, {'client_status': {'mobile': 'online'}}),
    ):
        data = put_statuses(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
