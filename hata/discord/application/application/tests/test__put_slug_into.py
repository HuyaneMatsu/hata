import vampytest

from ..fields import put_slug_into


def test__put_slug_into():
    """
    Tests whether ``put_slug_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {}),
        ('https://orindance.party/', False, {'slug': 'https://orindance.party/'}),
    ):
        data = put_slug_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
