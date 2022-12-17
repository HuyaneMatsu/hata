import vampytest

from ..fields import parse_party_id


def test__parse_party_id():
    """
    Tests whether ``parse_party_id`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'party_id': None}, None),
        ({'party_id': ''}, None),
        ({'party_id': 'a'}, 'a'),
    ):
        output = parse_party_id(input_data)
        vampytest.assert_eq(output, expected_output)
