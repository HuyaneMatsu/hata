import vampytest

from ...core import BUILTIN_EMOJIS, FORUM_TAGS
from ...emoji import create_partial_emoji_from_data, put_partial_emoji_data_into

from .. import ForumTag


def test__ForumTag__from_data__0():
    """
    Tests whether ``ForumTag.from_data`` works as intended.
    
    Case: cache and fields.
    """
    forum_tag_id = 202209090005
    emoji = BUILTIN_EMOJIS['heart']
    name = 'EMOTiON'
    moderated = True
    
    data = {
        'id': str(forum_tag_id),
        'name': name,
        'moderated': moderated,
    }
    
    put_partial_emoji_data_into(data, emoji)
    
    forum_tag = ForumTag.from_data(data)
    
    vampytest.assert_instance(forum_tag, ForumTag)
    vampytest.assert_eq(forum_tag.id, forum_tag_id)
    
    vampytest.assert_in(forum_tag_id, FORUM_TAGS)
    vampytest.assert_is(FORUM_TAGS[forum_tag_id], forum_tag)
    
    vampytest.assert_eq(forum_tag.name, name)
    vampytest.assert_is(forum_tag.emoji, emoji)
    vampytest.assert_eq(forum_tag.moderated, moderated)


def test__ForumTag__from_data__1():
    """
    Tests whether ``ForumTag.from_data`` works as intended.
    
    Case: duplicate call.
    """
    forum_tag_id = 202209090006
    
    data = {
        'id': str(forum_tag_id),
        'emoji_name': None,
        'name': ''
    }
    
    forum_tag = ForumTag.from_data(data)
    new_forum_tag = ForumTag.from_data(data)
    
    vampytest.assert_is(forum_tag, new_forum_tag)


def test__ForumTag__update_attributes():
    """
    Tests whether ``ForumTag._update_attributes`` works as intended.
    """
    old_emoji = BUILTIN_EMOJIS['heart']
    new_emoji = BUILTIN_EMOJIS['x']
    old_name = 'EMOTiON'
    new_name = 'EMPEROR'
    old_moderated = True
    new_moderated = False
    
    forum_tag = ForumTag(old_name, emoji = old_emoji, moderated = old_moderated)
    
    data = {
        'name': new_name,
        'moderated': new_moderated,
    }
    
    put_partial_emoji_data_into(data, new_emoji)
    
    forum_tag._update_attributes(data)

    vampytest.assert_eq(forum_tag.name, new_name)
    vampytest.assert_is(forum_tag.emoji, new_emoji)
    vampytest.assert_eq(forum_tag.moderated, new_moderated)


def test__ForumTag__difference_update_attributes():
    """
    Tests whether ``ForumTag._difference_update_attributes`` works as intended.
    """
    old_emoji = BUILTIN_EMOJIS['heart']
    new_emoji = BUILTIN_EMOJIS['x']
    old_name = 'EMOTiON'
    new_name = 'EMPEROR'
    old_moderated = True
    new_moderated = False
    
    forum_tag = ForumTag(old_name, emoji = old_emoji, moderated = old_moderated)
    
    data = {
        'name': new_name,
        'moderated': new_moderated,
    }
    
    put_partial_emoji_data_into(data, new_emoji)
    
    old_attributes = forum_tag._difference_update_attributes(data)

    vampytest.assert_eq(forum_tag.name, new_name)
    vampytest.assert_is(forum_tag.emoji, new_emoji)
    vampytest.assert_eq(forum_tag.moderated, new_moderated)
    
    vampytest.assert_in('name', old_attributes)
    vampytest.assert_in('emoji', old_attributes)
    vampytest.assert_in('moderated', old_attributes)
    
    vampytest.assert_eq(old_attributes['name'], old_name)
    vampytest.assert_is(old_attributes['emoji'], old_emoji)
    vampytest.assert_eq(old_attributes['moderated'], old_moderated)


def test__ForumTag__to_data():
    """
    Tests whether 
    """
    emoji = BUILTIN_EMOJIS['heart']
    name = 'EMOTiON'
    moderated = True
    
    forum_tag = ForumTag(name, emoji = emoji, moderated = moderated)
    
    data = forum_tag.to_data()
    
    vampytest.assert_in('name', data)
    vampytest.assert_in('moderated', data)
    vampytest.assert_in('emoji_name', data)
    
    vampytest.assert_eq(data['name'], name)
    vampytest.assert_eq(data['moderated'], moderated)
    
    vampytest.assert_is(create_partial_emoji_from_data(data), emoji)
    
