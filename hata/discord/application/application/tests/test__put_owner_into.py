import vampytest

from ....user import User, ZEROUSER

from ...team import Team

from ..fields import put_owner_into


def test__put_owner_into():
    """
    Tests whether ``put_owner_into`` works as intended.
    """
    user = User.precreate(202211270016)
    team = Team.precreate(202211270017)
    
    for input_value, defaults, expected_output in (
        (ZEROUSER, False, {}),
        (ZEROUSER, True, {'owner': None, 'team': None}),
        (user, True, {'owner': user.to_data(defaults = True, include_internals = True), 'team': None}),
        (team, True, {'owner': team.to_data_user(), 'team': team.to_data(defaults = True, include_internals = True)}),
    ):
        output = put_owner_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
