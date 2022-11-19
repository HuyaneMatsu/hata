import vampytest

from ..fields import parse_excluded_keywords


def test__parse_excluded_keywords():
    """
    Tests whether ``parse_excluded_keywords`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'allow_list': None}, None),
        ({'allow_list': []}, None),
        ({'allow_list': ['a']}, ('a', )),
    ):
        output = parse_excluded_keywords(input_data)
        vampytest.assert_eq(output, expected_output)
