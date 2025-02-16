import vampytest

from ..fields import put_discriminator


def test__put_discriminator():
    """
    Tests whether ``put_discriminator`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (0, False, {'discriminator': '0000'}),
        (69, False, {'discriminator': '0069'}),
        (7777, False, {'discriminator': '7777'}),
    ):
        data = put_discriminator(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
