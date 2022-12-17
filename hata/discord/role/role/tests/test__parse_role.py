import vampytest

from ....guild import Guild
from ....message import Message

from ..role import Role
from ..utils import parse_role


def test__parse_role():
    """
    Tests whether ``parse_role`` works as intended.
    """
    role_id_1 = 202211050004
    role_id_2 = 202211050005
    guild_id = 202211050006
    message_id = 202211050007
    
    name = 'fat dragon'
    message = Message.precreate(message_id, guild_id = guild_id)
    
    role = Role.precreate(role_id_1,guild_id = guild_id, name = name)
    guild = Guild.precreate(guild_id)
    guild.roles[role.id] = role
    
    for input_value, expected_output in (
        ('ayaya', None),
        
        (str(role_id_2), None),
        (str(role_id_1), role),
        
        (role.mention.replace(str(role_id_1), str(role_id_2)), None),
        (role.mention, role),
        
        (name, role),
        (name[:3], role),
    ):
        output = parse_role(input_value, message)
        vampytest.assert_is(output, expected_output)
