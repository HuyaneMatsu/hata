import vampytest

from ..fields import put_metadata_values_into


def test__put_metadata_values_into():
    """
    Tests whether ``put_metadata_values_into`` works as intended.
    """
    for input_value, defaults, expected_data in (
        (None, False, {}),
        (None, True, {'metadata': {}}),
        ({'a': 'b'}, False, {'metadata': {'a': 'b'}}),
    ):
        data = put_metadata_values_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_data)
