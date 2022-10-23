import vampytest

from ..fields import put_default_into


def test__put_default_into():
    """
    Tests whether ``put_default_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'default': False}),
        (True, False, {'default': True}),
    ):
        data = put_default_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
