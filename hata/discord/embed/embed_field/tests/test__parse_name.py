import vampytest

from ..fields import parse_name


def test__parse_name():
    """
    Tests whether ``parse_name`` works as intended.
    """
    for input_data, expected_output in (
        ({'name': None}, None),
        ({'name': ''}, None),
        ({'name': 'a'}, 'a'),
    ):
        output = parse_name(input_data)
        vampytest.assert_eq(output, expected_output)
