import warnings as module_warnings

import vampytest

from ....emoji import Emoji
from ....role import Role, RoleManagerType

from ..emoji_counts import EmojiCounts


def _assert_is_every_attribute_set(emoji_counts):
    """
    Asserts whether every attributes are set of the given emoji counts.
    
    Parameters
    ----------
    emoji_counts : ``EmojiCounts``
        The emoji counts to check out.
    """
    vampytest.assert_instance(emoji_counts, EmojiCounts)
    vampytest.assert_instance(emoji_counts.managed_animated, int)
    vampytest.assert_instance(emoji_counts.managed_static, int)
    vampytest.assert_instance(emoji_counts.normal_animated, int)
    vampytest.assert_instance(emoji_counts.normal_static, int)
    vampytest.assert_instance(emoji_counts.premium_animated, int)
    vampytest.assert_instance(emoji_counts.premium_static, int)


def _assert_empty(emoji_counts):
    """
    Asserts whether the given emoji joints are empty.
    
    Parameters
    ----------
    emoji_counts : ``EmojiCounts``
        The emoji counts to check out.
    """
    vampytest.assert_eq(emoji_counts.managed_animated, 0)
    vampytest.assert_eq(emoji_counts.managed_static, 0)
    vampytest.assert_eq(emoji_counts.normal_animated, 0)
    vampytest.assert_eq(emoji_counts.normal_static, 0)
    vampytest.assert_eq(emoji_counts.premium_animated, 0)
    vampytest.assert_eq(emoji_counts.premium_static, 0)
    

def test__EmojiCounts__new__0():
    """
    Tests whether ``EmojiCounts.__new__`` works as intended.
    
    Case: No fields given.
    """
    emoji_counts = EmojiCounts()
    _assert_is_every_attribute_set(emoji_counts)
    _assert_empty(emoji_counts)


def test__EmojiCounts__new__1():
    """
    Tests whether ``EmojiCounts.__new__`` works as intended.
    
    Case: All fields given.
    """
    managed_animated = 1
    managed_static = 2
    normal_animated = 3
    normal_static = 4
    premium_animated = 5
    premium_static = 6
    
    emoji_counts = EmojiCounts(
        managed_animated = managed_animated,
        managed_static = managed_static,
        normal_animated = normal_animated,
        normal_static = normal_static,
        premium_animated = premium_animated,
        premium_static = premium_static,
    )
    _assert_is_every_attribute_set(emoji_counts)
    
    vampytest.assert_eq(emoji_counts.managed_animated, managed_animated)
    vampytest.assert_eq(emoji_counts.managed_static, managed_static)
    vampytest.assert_eq(emoji_counts.normal_animated, normal_animated)
    vampytest.assert_eq(emoji_counts.normal_static, normal_static)
    vampytest.assert_eq(emoji_counts.premium_animated, premium_animated)
    vampytest.assert_eq(emoji_counts.premium_static, premium_static)


def test__EmojiCounts__from_emojis__0():
    """
    Tests whether ``EmojiCounts.from_emojis`` works as intended.
    
    Case: Empty iterable given.
    """
    emoji_counts = EmojiCounts.from_emojis([])
    _assert_is_every_attribute_set(emoji_counts)
    _assert_empty(emoji_counts)


def test__EmojiCounts__from_emojis__1():
    """
    Tests whether ``EmojiCounts.from_emojis`` works as intended.
    
    Case: Stuffed iterable given.
    """
    role = Role.precreate(202212190010, manager_type = RoleManagerType.subscription)
    
    managed_animated_ids = (202212190011,)
    managed_static_ids = (202212190012, 202212190013)
    normal_animated_ids = (202212190014, 202212190015, 202212190016)
    normal_static_ids = (202212190017, 202212190018, 202212190019, 202212190020)
    premium_animated_ids = (202212190021, 202212190022, 202212190023, 202212190024, 202212190025)
    premium_static_ids = (202212190026, 202212190027, 202212190028, 202212190029, 202212190030, 202212190031)
    
    emojis = [
        *(Emoji.precreate(emoji_id, animated = True, managed = True) for emoji_id in managed_animated_ids),
        *(Emoji.precreate(emoji_id, animated = False, managed = True) for emoji_id in managed_static_ids),
        *(Emoji.precreate(emoji_id, animated = True) for emoji_id in normal_animated_ids),
        *(Emoji.precreate(emoji_id, animated = False) for emoji_id in normal_static_ids),
        *(Emoji.precreate(emoji_id, animated = True, roles = [role]) for emoji_id in premium_animated_ids),
        *(Emoji.precreate(emoji_id, animated = False, roles = [role]) for emoji_id in premium_static_ids),
    ]
    
    
    emoji_counts = EmojiCounts.from_emojis(emojis)
    _assert_is_every_attribute_set(emoji_counts)
    
    
    vampytest.assert_eq(emoji_counts.managed_animated, len(managed_animated_ids))
    vampytest.assert_eq(emoji_counts.managed_static, len(managed_static_ids))
    vampytest.assert_eq(emoji_counts.normal_animated, len(normal_animated_ids))
    vampytest.assert_eq(emoji_counts.normal_static, len(normal_static_ids))
    vampytest.assert_eq(emoji_counts.premium_animated, len(premium_animated_ids))
    vampytest.assert_eq(emoji_counts.premium_static, len(premium_static_ids))


def test__EmojiCounts__managed_total():
    """
    Tests whether ``EmojiCounts.managed_total`` works as intended.
    """
    managed_animated = 1
    managed_static = 2
    
    expected_value = managed_animated + managed_static
    
    emoji_counts = EmojiCounts(
        managed_animated = managed_animated,
        managed_static = managed_static,
    )
    vampytest.assert_eq(emoji_counts.managed_total, expected_value)


def test__EmojiCounts__normal_total():
    """
    Tests whether ``EmojiCounts.normal_total`` works as intended.
    """
    normal_animated = 1
    normal_static = 2
    
    expected_value = normal_animated + normal_static
    
    emoji_counts = EmojiCounts(
        normal_animated = normal_animated,
        normal_static = normal_static,
    )
    vampytest.assert_eq(emoji_counts.normal_total, expected_value)


def test__EmojiCounts__premium_total():
    """
    Tests whether ``EmojiCounts.premium_total`` works as intended.
    """
    premium_animated = 1
    premium_static = 2
    
    expected_value = premium_animated + premium_static
    
    emoji_counts = EmojiCounts(
        premium_animated = premium_animated,
        premium_static = premium_static,
    )
    vampytest.assert_eq(emoji_counts.premium_total, expected_value)


def test__EmojiCounts__animated_total():
    """
    Tests whether ``EmojiCounts.animated_total`` works as intended.
    """
    managed_animated = 1
    normal_animated = 2
    premium_animated = 4
    
    expected_value = managed_animated + normal_animated + premium_animated
    
    emoji_counts = EmojiCounts(
        managed_animated = managed_animated,
        normal_animated = normal_animated,
        premium_animated = premium_animated,
    )
    vampytest.assert_eq(emoji_counts.animated_total, expected_value)


def test__EmojiCounts__static_total():
    """
    Tests whether ``EmojiCounts.static_total`` works as intended.
    """
    managed_static = 1
    normal_static = 2
    premium_static = 4
    
    expected_value = managed_static + normal_static + premium_static
    
    emoji_counts = EmojiCounts(
        managed_static = managed_static,
        normal_static = normal_static,
        premium_static = premium_static,
    )
    vampytest.assert_eq(emoji_counts.static_total, expected_value)



def test__EmojiCounts__total():
    """
    Tests whether ``EmojiCounts.total`` works as intended.
    """
    managed_animated = 1
    managed_static = 2
    normal_animated = 4
    normal_static = 8
    premium_animated = 16
    premium_static = 32
    
    expected_value = (
        managed_animated + managed_static + normal_animated + normal_static + premium_animated + premium_static
    )
    
    emoji_counts = EmojiCounts(
        managed_animated = managed_animated,
        managed_static = managed_static,
        normal_animated = normal_animated,
        normal_static = normal_static,
        premium_animated = premium_animated,
        premium_static = premium_static,
    )
    vampytest.assert_eq(emoji_counts.total, expected_value)


def test__EmojiCounts__bool():
    """
    Tests whether ``EmojiCounts.__bool__`` works as intended.
    """
    for keyword_parameters, expected_output in (
        ({}, False),
        ({'managed_animated': 1}, True),
        ({'managed_static': 1}, True),
        ({'normal_animated': 1}, True),
        ({'normal_static': 1}, True),
        ({'premium_animated': 1}, True),
        ({'premium_static': 1}, True),
    ):
        emoji_counts = EmojiCounts(**keyword_parameters)
        vampytest.assert_eq(bool(emoji_counts), expected_output)


def test__EmojiCounts__repr():
    """
    Tests whether ``EmojiCounts.__repr__`` works as intended.
    """
    managed_animated = 1
    managed_static = 2
    normal_animated = 3
    normal_static = 4
    premium_animated = 5
    premium_static = 6
    
    emoji_counts = EmojiCounts(
        managed_animated = managed_animated,
        managed_static = managed_static,
        normal_animated = normal_animated,
        normal_static = normal_static,
        premium_animated = premium_animated,
        premium_static = premium_static,
    )
    
    vampytest.assert_instance(repr(emoji_counts), str)


def test__EmojiCounts__eq():
    """
    Tests whether ``EmojiCounts.__eq__`` works as intended.
    """
    managed_animated = 1
    managed_static = 2
    normal_animated = 3
    normal_static = 4
    premium_animated = 5
    premium_static = 6
    
    keyword_parameters = {
        'managed_animated': managed_animated,
        'managed_static': managed_static,
        'normal_animated': normal_animated,
        'normal_static': normal_static,
        'premium_animated': premium_animated,
        'premium_static': premium_static,
    }
    
    emoji_counts = EmojiCounts(**keyword_parameters)
    
    vampytest.assert_eq(emoji_counts, emoji_counts)
    vampytest.assert_ne(emoji_counts, object())
    
    for field_name, field_value in (
        ('managed_animated', 7),
        ('managed_static', 8),
        ('normal_animated', 9),
        ('normal_static', 10),
        ('premium_animated', 11),
        ('premium_static', 12),

    ):
        test_emoji_counts = EmojiCounts(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(emoji_counts, test_emoji_counts)


def test__EmojiCounts__hash():
    """
    Tests whether ``EmojiCounts.__hash__`` works as intended.
    """
    managed_animated = 1
    managed_static = 2
    normal_animated = 3
    normal_static = 4
    premium_animated = 5
    premium_static = 6
    
    emoji_counts = EmojiCounts(
        managed_animated = managed_animated,
        managed_static = managed_static,
        normal_animated = normal_animated,
        normal_static = normal_static,
        premium_animated = premium_animated,
        premium_static = premium_static,
    )
    
    vampytest.assert_instance(hash(emoji_counts), int)


def test__EmojiCounts__iter():
    """
    Tests whether ``EmojiCounts.__iter__`` works as intended. This field is deprecated.
    """
    managed_animated = 1
    managed_static = 2
    normal_animated = 3
    normal_static = 4
    
    emoji_counts = EmojiCounts(
        managed_animated = managed_animated,
        managed_static = managed_static,
        normal_animated = normal_animated,
        normal_static = normal_static,
    )
    
    with module_warnings.catch_warnings(record = True) as warnings:
        module_warnings.simplefilter('always')
        
        unpacked = [*emoji_counts]
        
        vampytest.assert_eq(len(warnings), 1)
    
    vampytest.assert_eq(unpacked, [normal_static, normal_animated, managed_static, managed_animated])
