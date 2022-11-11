import vampytest

from ..fields import put_custom_id_into


def test__put_custom_id_into():
    """
    Tests whether ``put_custom_id_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'custom_id': None}),
        ('a', False, {'custom_id': 'a'}),
    ):
        data = put_custom_id_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
