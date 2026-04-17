import vampytest

from ....user import User

from ..ban_entry import BanEntry


def test__BanEntry__repr():
    """
    Tests whether ``BanEntry.__repr__`` works as intended.
    """
    reason = 'hey mister'
    user = User.precreate(202405010006, name = 'Yuuka')
    
    ban_entry = BanEntry(
        reason = reason,
        user = user,
    )
    
    vampytest.assert_instance(repr(ban_entry), str)


def test__BanEntry__hash():
    """
    Tests whether ``BanEntry.__hash__`` works as intended.
    """
    reason = 'hey mister'
    user = User.precreate(202405010007, name = 'Yuuka')
    
    ban_entry = BanEntry(
        reason = reason,
        user = user,
    )
    
    vampytest.assert_instance(hash(ban_entry), int)


def test__BanEntry__eq():
    """
    Tests whether ``BanEntry.__repr__`` works as intended.
    """
    reason = 'hey mister'
    user = User.precreate(202405010008, name = 'Yuuka')
    
    keyword_parameters = {
        'reason': reason,
        'user': user,
    }
    
    ban_entry = BanEntry(**keyword_parameters)
    
    vampytest.assert_eq(ban_entry, ban_entry)
    vampytest.assert_ne(ban_entry, object())
    
    for field_name, field_value in (
        ('reason', None),
        ('user', User.precreate(202305170022, name = 'Satori')),
    ):
        ban_entry_altered = BanEntry(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(ban_entry, ban_entry_altered)


def test__BanEntry__unpack():
    """
    Tests whether ``BanEntry`` unpacking works as intended.
    """
    reason = 'hey mister'
    user = User.precreate(202405010009, name = 'Yuuka')
    
    ban_entry = BanEntry(
        reason = reason,
        user = user,
    )
    
    vampytest.assert_eq(len([*ban_entry]), len(ban_entry))
