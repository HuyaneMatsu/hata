import vampytest

from ..fields import parse_version


def test__parse_version():
    """
    Tests whether ``parse_version`` works as intended.
    """
    version = 202302260009
    
    for input_data, expected_output in (
        ({}, 0),
        ({'version': None}, 0),
        ({'version': str(version)}, version),
    ):
        output = parse_version(input_data)
        vampytest.assert_eq(output, expected_output)
