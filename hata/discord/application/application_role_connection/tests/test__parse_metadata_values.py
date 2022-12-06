import vampytest

from ..fields import parse_metadata_values


def test__parse_metadata_values():
    """
    Tests whether ``parse_metadata_values`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'metadata': None}, None),
        ({'metadata': {}}, None),
        ({'metadata': {'a': 'b'}}, {'a': 'b'}),
    ):
        output = parse_metadata_values(input_data)
        vampytest.assert_eq(output, expected_output)
