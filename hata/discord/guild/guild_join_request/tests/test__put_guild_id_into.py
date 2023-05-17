import vampytest

from ..fields import put_guild_id_into


def test__put_guild_id_into():
    """
    Tests whether ``put_guild_id_into`` is working as intended.
    """
    guild_id = 202305160040
    
    for input_value, defaults, expected_output in (
        (guild_id, False, {'guild_id': str(guild_id)}),
    ):
        data = put_guild_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
