import vampytest

from ..fields import put_renewal_into


def test__put_renewal_into():
    """
    Tests whether ``put_renewal_into`` works as intended.
    """
    for input_, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'is_renewal': False}),
        (True, False, {'is_renewal': True}),
    ):
        data = put_renewal_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
