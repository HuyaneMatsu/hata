import vampytest

from ....user import ClientUserBase, User

from ..ban_entry import BanEntry


def _assert_fields_set(ban_entry):
    """
    Checks whether every attribute is set of the given ban entry.
    
    Parameters
    ----------
    ban_entry : ``BanEntry``
        The ban entry to check.
    """
    vampytest.assert_instance(ban_entry, BanEntry)
    vampytest.assert_instance(ban_entry.reason, str, nullable = True)
    vampytest.assert_instance(ban_entry.user, ClientUserBase)


def test__BanEntry__new__all_fields():
    """
    Tests whether ``BanEntry.__new__`` works as intended.
    
    Case: Fields given.
    """
    reason = 'hey mister'
    user = User.precreate(202405010003, name = 'Yuuka')
    
    ban_entry = BanEntry(user, reason)
    
    _assert_fields_set(ban_entry)
    
    vampytest.assert_eq(ban_entry.reason, reason)
    vampytest.assert_is(ban_entry.user, user)
