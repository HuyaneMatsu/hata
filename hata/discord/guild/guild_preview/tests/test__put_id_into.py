import vampytest

from ..fields import put_id_into


def test__put_id_into():
    """
    Tests whether ``put_id_into`` works as intended.
    """
    guild_id = 202301080006
    
    for input_value, defaults, expected_output in (
        (guild_id, False, {'id': str(guild_id)}),
    ):
        data = put_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
