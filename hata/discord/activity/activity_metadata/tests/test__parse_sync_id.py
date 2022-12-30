import vampytest

from ..fields import parse_sync_id


def test__parse_sync_id():
    """
    Tests whether ``parse_sync_id`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'sync_id': None}, None),
        ({'sync_id': ''}, None),
        ({'sync_id': 'a'}, 'a'),
    ):
        output = parse_sync_id(input_data)
        vampytest.assert_eq(output, expected_output)
