import vampytest

from ..fields import put_height_into


def test__put_height_into():
    """
    Tests whether ``put_height_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (0, False, {'height': 0}),
    ):
        data = put_height_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
