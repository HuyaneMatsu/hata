import vampytest

from ..fields import put_party_id


def test__put_party_id():
    """
    Tests whether ``put_party_id`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {'party_id': ''}),
        ('', False, {'party_id': ''}),
        ('a', False, {'party_id': 'a'}),
    ):
        data = put_party_id(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
