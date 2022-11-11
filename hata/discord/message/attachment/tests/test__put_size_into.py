import vampytest

from ..fields import put_size_into


def test__put_size_into():
    """
    Tests whether ``put_size_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (0, False, {'size': 0}),
    ):
        data = put_size_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
