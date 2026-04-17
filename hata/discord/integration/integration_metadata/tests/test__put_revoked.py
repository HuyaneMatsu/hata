import vampytest

from ..fields import put_revoked


def test__put_revoked():
    """
    Tests whether ``put_revoked`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'revoked': False}),
        (True, False, {'revoked': True}),
    ):
        data = put_revoked(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
