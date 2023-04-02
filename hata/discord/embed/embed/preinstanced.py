__all__ = ('EmbedType',)

from ...bases import Preinstance as P, PreinstancedBase


class EmbedType(PreinstancedBase):
    """
    Represents an embed's type.
    
    Attributes
    ----------
    value : `str`
        The discord side identifier value of the embed type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``EmbedType``) items
        Stores the predefined embed types in `value` - `embed_type` relation.
        This container is accessed when converting an embed type to it's representation.
    VALUE_TYPE : `type` = `str`
        The embed types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the embed types.
    
    Each predefined embed type instance can also be accessed as class attribute:
    
    +---------------------------+---------------------------+---------------------------+
    | Class attribute name      | Name                      | Value                     |
    +===========================+===========================+===========================+
    | application_news          | application news          | application_news          |
    +---------------------------+---------------------------+---------------------------+
    | article                   | article                   | article                   |
    +---------------------------+---------------------------+---------------------------+
    | auto_moderation_message   | auto moderation message   | auto_moderation_message   |
    +---------------------------+---------------------------+---------------------------+
    | gifv                      | gifv                      | gifv                      |
    +---------------------------+---------------------------+---------------------------+
    | image                     | image                     | image                     |
    +---------------------------+---------------------------+---------------------------+
    | link                      | link                      | link                      |
    +---------------------------+---------------------------+---------------------------+
    | rich                      | rich                      | rich                      |
    +---------------------------+---------------------------+---------------------------+
    | tweet                     | tweet                     | tweet                     |
    +---------------------------+---------------------------+---------------------------+
    | video                     | video                     | video                     |
    +---------------------------+---------------------------+---------------------------+
    """
    INSTANCES = {}
    VALUE_TYPE = str
    
    __slots__ = ()
    
    # predefined
    application_news = P('application_news', 'application news')
    article = P('article', 'article')
    auto_moderation_message = P('auto_moderation_message', 'auto moderation message')
    gifv = P('gifv', 'gifv')
    image = P('image', 'image')
    link = P('link', 'link')
    rich = P('rich', 'rich')
    tweet = P('tweet', 'tweet')
    video = P('video', 'video')
