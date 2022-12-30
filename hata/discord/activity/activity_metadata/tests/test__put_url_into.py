import vampytest

from ..fields import put_url_into


def test__put_url_into():
    """
    Tests whether ``put_url_into`` works as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {}),
        ('https://orindance.party/', False, {'url': 'https://orindance.party/'}),
    ):
        data = put_url_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
