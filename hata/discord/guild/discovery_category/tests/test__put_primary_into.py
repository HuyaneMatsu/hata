import vampytest

from ..fields import put_primary_into


def test__put_primary_into():
    """
    Tests whether ``put_primary_into`` works as intended.
    """
    for input_, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'is_primary': False}),
        (True, False, {'is_primary': True}),
    ):
        data = put_primary_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
