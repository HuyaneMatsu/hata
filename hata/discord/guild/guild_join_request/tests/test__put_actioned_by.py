import vampytest

from ....user import User

from ..fields import put_actioned_by


def test__put_actioned_by():
    """
    Tests whether ``put_actioned_by`` is working as intended.
    """
    user = User.precreate(202305160043, name = 'East')
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'actioned_by_user': None}),
        (user, True, {'actioned_by_user': user.to_data(defaults = True, include_internals = True)}),
    ):
        data = put_actioned_by(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
