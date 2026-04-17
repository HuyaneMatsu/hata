import vampytest

from ..fields import put_creator_id


def test__put_creator_id():
    """
    Tests whether ``put_creator_id`` is working as intended.
    """
    creator_id = 202211170027
    
    for input_, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'creator_id': None}),
        (creator_id, False, {'creator_id': str(creator_id)}),
    ):
        data = put_creator_id(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
