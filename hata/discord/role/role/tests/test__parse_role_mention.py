import vampytest

from ..role import Role
from ..utils import parse_role_mention


def test__parse_role_mention():
    """
    Tests whether ``parse_role_mention`` works as intended.
    """
    role_id_1 = 202211050002
    role_id_2 = 202211050003
    
    role = Role.precreate(role_id_1)
    
    for input_value, expected_output in (
        ('ayaya', None),
        (role.mention.replace(str(role_id_1), str(role_id_2)), None),
        (role.mention, role)
    ):
        output = parse_role_mention(input_value)
        vampytest.assert_is(output, expected_output)
