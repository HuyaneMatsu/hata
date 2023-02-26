import vampytest

from ..fields import put_version_into


def test__put_version_into():
    """
    Tests whether ``put_version_into`` works as intended.
    """
    version = 202302260010
    
    for input_value, defaults, expected_output in (
        (version, False, {'version': str(version)}),
    ):
        data = put_version_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
