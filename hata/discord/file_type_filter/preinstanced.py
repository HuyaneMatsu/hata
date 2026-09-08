__all__ = ('FileTypeFilterGroup',)

from scarletio import copy_docs

from ..bases import Preinstance as P, PreinstancedBase


class FileTypeFilterGroup(PreinstancedBase, value_type = str):
    """
    Represents a file type group
    
    Attributes
    ----------
    name : `str`
        The name of the schedule week's day
    
    value : `str`
        The unique identifier of the schedule week's day
    
    members : `None | tuple<str>`
        The members of the group.
    
    Type Attributes
    ---------------
    Each type filter group can also be access as a type attribute as well
    
    +-----------------------+-----------+-----------------------+---------------------------------------+
    | Class Attribute name  | value     | name                  | members                               |
    +=======================+===========+=======================+=======================================+
    | audio                 | audio     | audio                 | flac, m4a, wav, mp3, ogg, opus        |
    +-----------------------+-----------+-----------------------+---------------------------------------+
    | image                 | image     | image                 | avif, gif, jfif, jpeg, jpg, png, webp |
    +-----------------------+-----------+-----------------------+---------------------------------------+
    | video                 | video     | video                 | ov, mp4, qt, webm                     |
    +-----------------------+-----------+-----------------------+---------------------------------------+
    """
    __slots__ = ('members',)
    
    
    @copy_docs(PreinstancedBase.__new__)
    def __new__(cls, value, name = None, members = None):
        if name is None:
            name = value.casefold().replace('_', ' ')
        
        instance = PreinstancedBase.__new__(cls, value, name)
        instance.members = members
        return instance
    
    
    audio = P('audio', 'audio', ('flac', 'm4a', 'wav', 'mp3', 'ogg', 'opus'))
    image = P('image', 'image', ('avif', 'gif', 'jfif', 'jpeg', 'jpg', 'png', 'webp'))
    video = P('video', 'video', ('mov', 'mp4', 'qt', 'webm'))
