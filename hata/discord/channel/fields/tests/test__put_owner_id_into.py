import vampytest


from ..owner_id import put_owner_id_into


def test__put_owner_id_into():
    """
    Tests whether ``put_owner_id_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'owner_id': None}),
        (1, False, {'owner_id': '1'}),
    ):
        data = put_owner_id_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
