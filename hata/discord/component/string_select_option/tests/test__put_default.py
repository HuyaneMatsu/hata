import vampytest

from ..fields import put_default


def test__put_default():
    """
    Tests whether ``put_default`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'default': False}),
        (True, False, {'default': True}),
    ):
        data = put_default(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
