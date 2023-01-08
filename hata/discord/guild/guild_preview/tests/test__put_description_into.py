import vampytest

from ..fields import put_description_into


def test__put_description_into():
    """
    Tests whether ``put_description_into`` works as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {'description': ''}),
        ('a', False, {'description': 'a'}),
    ):
        data = put_description_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
