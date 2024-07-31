__all__ = ('EmbedType',)

from ...bases import Preinstance as P, PreinstancedBase


class EmbedType(PreinstancedBase):
    """
    Represents an embed's type.
    
    Attributes
    ----------
    name : `str`
        The embed type's name.
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
    
    +-------------------------------+-------------------------------+-------------------------------+
    | Class attribute name          | Name                          | Value                         |
    +===============================+===============================+===============================+
    | application_news              | application news              | application_news              |
    +-------------------------------+-------------------------------+-------------------------------+
    | article                       | article                       | article                       |
    +-------------------------------+-------------------------------+-------------------------------+
    | auto_moderation_message       | auto moderation message       | auto_moderation_message       |
    +-------------------------------+-------------------------------+-------------------------------+
    | auto_moderation_notification  | auto moderation notification  | auto_moderation_notification  |
    +-------------------------------+-------------------------------+-------------------------------+
    | gift                          | gift                          | gift                          |
    +-------------------------------+-------------------------------+-------------------------------+
    | gifv                          | gifv                          | gifv                          |
    +-------------------------------+-------------------------------+-------------------------------+
    | image                         | image                         | image                         |
    +-------------------------------+-------------------------------+-------------------------------+
    | poll_result                   | poll result                   | poll_result                   |
    +-------------------------------+-------------------------------+-------------------------------+
    | post_preview                  | post preview                  | post_preview                  |
    +-------------------------------+-------------------------------+-------------------------------+
    | link                          | link                          | link                          |
    +-------------------------------+-------------------------------+-------------------------------+
    | rich                          | rich                          | rich                          |
    +-------------------------------+-------------------------------+-------------------------------+
    | safety_policy_notice          | safety policy notice          | safety_policy_notice          |
    +-------------------------------+-------------------------------+-------------------------------+
    | text                          | text                          | text                          |
    +-------------------------------+-------------------------------+-------------------------------+
    | tweet                         | tweet                         | tweet                         |
    +-------------------------------+-------------------------------+-------------------------------+
    | video                         | video                         | video                         |
    +-------------------------------+-------------------------------+-------------------------------+
    """
    INSTANCES = {}
    VALUE_TYPE = str
    
    __slots__ = ()
    
    # predefined
    application_news = P('application_news', 'application news')
    article = P('article', 'article')
    auto_moderation_message = P('auto_moderation_message', 'auto moderation message')
    auto_moderation_notification = P('auto_moderation_notification', 'auto moderation notification')
    gift = P('gift', 'gift')
    gifv = P('gifv', 'gifv')
    image = P('image', 'image')
    poll_result = P('poll_result', 'poll result')
    post_preview = P('post_preview', 'post preview')
    link = P('link', 'link')
    rich = P('rich', 'rich')
    safety_policy_notice = P('safety_policy_notice', 'safety policy notice')
    text = P('text', 'text')
    tweet = P('tweet', 'tweet')
    video = P('video', 'video')


EmbedType.INSTANCES[''] = EmbedType.rich
