import vampytest

from ....user import User, GuildProfile

from ..fields import put_user_into


def test__put_user_into():
    """
    Tests whether ``put_user_into`` works as intended.
    """
    user = User.precreate(202210280009)
    guild_profile = GuildProfile()
    serialize_guild_id = 202210280010
    user.guild_profiles[serialize_guild_id] = guild_profile
    
    
    for input_value, expected_output, guild_id in (
        (
            user,
            {
                'user': user.to_data(
                    defaults = True,
                    include_internals = True,
                )
            },
            0,
        ), (
            user,
            {
                'member': {
                    **guild_profile.to_data(
                        defaults = True,
                        include_internals = True,
                    ),
                    'user': user.to_data(
                        defaults = True,
                        include_internals = True,
                    )
                }
            },
            serialize_guild_id,
        )
        
    ):
        output = put_user_into(input_value, {}, True, guild_id = guild_id)
        vampytest.assert_eq(output, expected_output)
