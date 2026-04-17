import vampytest

from ..fields import put_invitable


def test__put_invitable():
    """
    Tests whether ``put_invitable`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (True, False, {}),
        (False, False, {'thread_metadata': {'invitable': False}}),
        (True, True, {'thread_metadata': {'invitable': True}}),
    ):
        data = put_invitable(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
