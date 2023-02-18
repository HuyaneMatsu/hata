import vampytest

from ..fields import put_id_into


def test__put_id_into():
    """
    Tests whether ``put_id_into`` works as intended.
    """
    forum_tag_id = 202302170001
    
    for input_value, defaults, expected_output in (
        (forum_tag_id, False, {'id': str(forum_tag_id)}),
    ):
        data = put_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
