import vampytest

from ..fields import put_party_id_into


def test__put_party_id_into():
    """
    Tests whether ``put_party_id_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {'party_id': ''}),
        ('', False, {'party_id': ''}),
        ('a', False, {'party_id': 'a'}),
    ):
        data = put_party_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
