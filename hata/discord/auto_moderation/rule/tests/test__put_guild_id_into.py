import vampytest

from ..fields import put_guild_id_into


def test__put_guild_id_into():
    """
    Tests whether ``put_guild_id_into`` is working as intended.
    """
    guild_id = 202211170028
    
    for input_, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'guild_id': None}),
        (guild_id, False, {'guild_id': str(guild_id)}),
    ):
        data = put_guild_id_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
