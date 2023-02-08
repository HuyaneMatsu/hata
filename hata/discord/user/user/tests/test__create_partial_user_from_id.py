import vampytest

from .. import User, create_partial_user_from_id


def test__create_partial_user_from_id():
    """
    Tests whether `create_partial_user_from_id` caches as expected.
    """
    user_id = 102
    
    user = create_partial_user_from_id(user_id)
    precreated = User.precreate(user_id)
    
    vampytest.assert_is(user, precreated)
