import vampytest

from ....user import User, ZEROUSER

from ...team import Team

from ..fields import parse_owner


def test__parse_owner():
    """
    Tests whether ``parse_owner`` works as intended.
    """
    user = User.precreate(202211270014)
    team = Team.precreate(202211270015)
    
    for input_data, expected_output in (
        ({}, ZEROUSER),
        ({'owner': None}, ZEROUSER),
        ({'team': None}, ZEROUSER),
        ({'owner': None, 'team': None}, ZEROUSER),
        ({'owner': user.to_data(defaults = True, include_internals = True), 'team': None}, user),
        ({'owner': None, 'team': team.to_data(defaults = True, include_internals = True)}, team),
    ):
        owner = parse_owner(input_data)
        vampytest.assert_is(owner, expected_output)
