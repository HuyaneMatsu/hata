import vampytest

from ..fields import parse_statuses


def test__parse_statuses():
    """
    Tests whether ``parse_statuses` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'client_status': None}, None),
        ({'client_status': {}}, None),
        ({'client_status': {'mobile': 'online'}}, {'mobile': 'online'}),
    ):
        output = parse_statuses(input_data)
        vampytest.assert_eq(output, expected_output)
