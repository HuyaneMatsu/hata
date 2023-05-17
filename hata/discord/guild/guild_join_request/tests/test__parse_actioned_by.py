import vampytest

from ....user import User

from ..fields import parse_actioned_by


def test__parse_actioned_by():
    """
    Tests whether ``parse_actioned_by`` works as intended.
    """
    user = User.precreate(202305160043, name = 'East')
    
    for input_data, expected_output in (
        ({}, None),
        ({'actioned_by_user': None}, None),
        ({'actioned_by_user': user.to_data(defaults = True, include_internals = True)}, user),
    ):
        output = parse_actioned_by(input_data)
        vampytest.assert_is(output, expected_output)
