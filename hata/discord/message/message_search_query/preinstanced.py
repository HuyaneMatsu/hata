__all__ = ('MessageSearchAuthorType', 'MessageSearchHasType', 'MessageSearchSortByType', 'MessageSearchSortOrderType')

from ...bases import Preinstance as P, PreinstancedBase


class MessageSearchAuthorType(PreinstancedBase, value_type = str):
    """
    Represents a message search author's type.
    
    Attributes
    ----------
    name : `str`
        The name of the message search author type.
    
    value : `str`
        The discord side identifier value of the message search author type.
    
    Type Attributes
    ---------------
    Every predefined message search author type can be accessed as type attribute as well:
    
    +-----------------------+---------------+---------------+
    | Type attribute name   | name          | value         |
    +=======================+===============+===============+
    | bot                   | bot           | 'bot'         |
    +-----------------------+---------------+---------------+
    | user                  | user          | 'user'        |
    +-----------------------+---------------+---------------+
    | webhook               | webhook       | 'webhook'     |
    +-----------------------+---------------+---------------+
    | no_bot                | no bot        | '-bot'        |
    +-----------------------+---------------+---------------+
    | no_user               | no user       | '-user'       |
    +-----------------------+---------------+---------------+
    | no_webhook            | no webhook    | '-webhook'    |
    +-----------------------+---------------+---------------+
    """
    __slots__ = ()
    
    # predefined
    none = P('', 'none')
    
    bot = P('bot', 'bot')
    user = P('user', 'user')
    webhook = P('webhook', 'webhook')
    
    no_bot = P('-bot', 'no bot')
    no_user = P('-user', 'no user')
    no_webhook = P('-webhook', 'no webhook')


class MessageSearchHasType(PreinstancedBase, value_type = str):
    """
    Represents a message search's has type.
    
    Attributes
    ----------
    name : `str`
        The name of the message search has type.
    
    value : `str`
        The discord side identifier value of the message search has type.
    
    Type Attributes
    ---------------
    Every predefined message search has type can be accessed as type attribute as well:
    
    +-----------------------+---------------+---------------+
    | Type attribute name   | name          | value         |
    +=======================+===============+===============+
    | none                  | none          | ''            |
    +-----------------------+---------------+---------------+
    | embed                 | embed         | 'embed'       |
    +-----------------------+---------------+---------------+
    | file                  | file          | 'file'        |
    +-----------------------+---------------+---------------+
    | image                 | image         | 'image'       |
    +-----------------------+---------------+---------------+
    | link                  | link          | 'link'        |
    +-----------------------+---------------+---------------+
    | poll                  | poll          | 'poll'        |
    +-----------------------+---------------+---------------+
    | snapshot              | snapshot      | 'snapshot'    |
    +-----------------------+---------------+---------------+
    | sound                 | sound         | 'sound'       |
    +-----------------------+---------------+---------------+
    | sticker               | sticker       | 'sticker'     |
    +-----------------------+---------------+---------------+
    | video                 | video         | 'video'       |
    +-----------------------+---------------+---------------+
    | no_embed              | no embed      | '-embed'      |
    +-----------------------+---------------+---------------+
    | no_file               | no file       | '-file'       |
    +-----------------------+---------------+---------------+
    | no_image              | no image      | '-image'      |
    +-----------------------+---------------+---------------+
    | no_link               | no link       | '-link'       |
    +-----------------------+---------------+---------------+
    | no_poll               | no poll       | '-poll'       |
    +-----------------------+---------------+---------------+
    | no_snapshot           | no snapshot   | '-snapshot'   |
    +-----------------------+---------------+---------------+
    | no_sound              | no sound      | '-sound'      |
    +-----------------------+---------------+---------------+
    | no_sticker            | no sticker    | '-sticker'    |
    +-----------------------+---------------+---------------+
    | no_video              | no video      | '-video'      |
    +-----------------------+---------------+---------------+
    """
    __slots__ = ()
    
    # predefined
    none = P('', 'none')
    
    embed = P('embed', 'embed')
    file = P('file', 'file')
    image = P('image', 'image')
    link = P('link', 'link')
    poll = P('poll', 'poll')
    snapshot = P('snapshot', 'snapshot')
    sound = P('sound', 'sound')
    sticker = P('sticker', 'sticker')
    video = P('video', 'video')
    
    no_embed = P('-embed', 'no embed')
    no_file = P('-file', 'no file')
    no_image = P('-image', 'no image')
    no_link = P('-link', 'no link')
    no_poll = P('-poll', 'no poll')
    no_snapshot = P('-snapshot', 'no snapshot')
    no_sound = P('-sound', 'no sound')
    no_sticker = P('-sticker', 'no sticker')
    no_video = P('-video', 'no video')


class MessageSearchSortByType(PreinstancedBase, value_type = str):
    """
    Represents a message search sort by's type.
    
    Attributes
    ----------
    name : `str`
        The name of the message search sort by type.
    
    value : `str`
        The discord side identifier value of the message search sort by type.
    
    Type Attributes
    ---------------
    Every predefined message search sort by type can be accessed as type attribute as well:
    
    +-----------------------+---------------+---------------+
    | Type attribute name   | name          | value         |
    +=======================+===============+===============+
    | creation             | creation       | 'timestamp'   |
    +-----------------------+---------------+---------------+
    | relevance             | relevance     | 'relevance'   |
    +-----------------------+---------------+---------------+
    """
    __slots__ = ()
    
    # predefined
    creation = P('creation', 'creation')
    relevance = P('relevance', 'relevance')


MessageSearchSortByType.INSTANCES[''] = MessageSearchSortByType.creation


class MessageSearchSortOrderType(PreinstancedBase, value_type = str):
    """
    Represents a message search sort order's type.
    
    Attributes
    ----------
    name : `str`
        The name of the message search sort order type.
    
    value : `str`
        The discord side identifier value of the message search sort order type.
    
    Type Attributes
    ---------------
    Every predefined message search sort order type can be accessed as type attribute as well:
    
    +-----------------------+---------------+---------------+
    | Type attribute name   | name          | value         |
    +=======================+===============+===============+
    | ascending             | ascending     | 'asc'         |
    +-----------------------+---------------+---------------+
    | descending            | descending    | 'desc'        |
    +-----------------------+---------------+---------------+
    """
    __slots__ = ()
    
    # predefined
    ascending = P('asc', 'ascending')
    descending = P('desc', 'descending')


MessageSearchSortOrderType.INSTANCES[''] = MessageSearchSortOrderType.descending
