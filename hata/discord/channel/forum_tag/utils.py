__all__ = ('create_forum_tag_from_id', )

from ...core import FORUM_TAGS

from .fields import (
    put_emoji_into, put_moderated_into, put_name_into, validate_emoji, validate_moderated, validate_name
)
from .forum_tag import ForumTag


FORUM_TAG_FIELD_CONVERTERS = {
    'emoji': (validate_emoji, put_emoji_into),
    'moderated': (validate_moderated, put_moderated_into),
    'name': (validate_name, put_name_into),
}


def create_forum_tag_from_id(forum_tag_id):
    """
    Creates a forum tag from the given identifier.
    
    Parameters
    ----------
    forum_tag_id : `int`
        The forum tag's identifier.
    
    Returns
    -------
    forum_tag : ``ForumTag``
    """
    try:
        forum_tag = FORUM_TAGS[forum_tag_id]
    except KeyError:
        forum_tag = ForumTag._create_empty(forum_tag_id)
        FORUM_TAGS[forum_tag_id] = forum_tag
    
    return forum_tag
