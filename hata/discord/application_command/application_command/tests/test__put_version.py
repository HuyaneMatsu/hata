import vampytest

from ..fields import put_version


def test__put_version():
    """
    Tests whether ``put_version`` works as intended.
    """
    version = 202302260010
    
    for input_value, defaults, expected_output in (
        (version, False, {'version': str(version)}),
    ):
        data = put_version(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
