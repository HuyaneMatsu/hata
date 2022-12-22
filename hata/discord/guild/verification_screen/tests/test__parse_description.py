import vampytest

from ..fields import parse_description


def test__parse_description():
    """
    Tests whether ``parse_description`` works as intended.
    """
    for input_data, expected_output in (
        ({'description': None}, None),
        ({'description': ''}, None),
        ({'description': 'a'}, 'a'),
    ):
        output = parse_description(input_data)
        vampytest.assert_eq(output, expected_output)
