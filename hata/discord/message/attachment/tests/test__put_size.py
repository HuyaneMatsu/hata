import vampytest

from ..fields import put_size


def test__put_size():
    """
    Tests whether ``put_size`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (0, False, {'size': 0}),
    ):
        data = put_size(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
