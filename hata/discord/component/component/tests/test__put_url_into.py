import vampytest

from ..fields import put_url_into


def test__put_url_into():
    """
    Tests whether ``put_url_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {}),
        ('orindance.party', False, {'url': 'orindance.party'}),
    ):
        data = put_url_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
