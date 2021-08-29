__all__ = ('reaction_mapping', 'reaction_mapping_line',)

from ...backend.export import include
from ...backend.utils import set_docs

from .utils import create_partial_emoji_from_data

Client = include('Client')


class reaction_mapping(dict):
    """
    A `dict` subclass, which contains the reactions on a ``Message`` with (``Emoji``, ``reaction_mapping_line``)
    items.
    
    Attributes
    ----------
    fully_loaded : `bool`
        Whether the reaction mapping line is fully loaded.
    """
    __slots__ = ('fully_loaded',)
    
    def __init__(self, data):
        """
        Fills the reaction mapping with the given data.
        
        Parameters
        ----------
        data : `None` or `dict` of (`str`, `Any`) items
        """
        if (data is None) or (not data):
            self.fully_loaded = True
            return
        
        self.fully_loaded = False
        for line in data:
            self[create_partial_emoji_from_data(line['emoji'])] = reaction_mapping_line(line.get('count', 1))
    
    emoji_count = set_docs(
        property(dict.__len__),
        """
        The amount of different emojis, which were added on the reaction mapping's respective ``Message``.
        
        Returns
        -------
        emoji_count : `int`
        """
    )
    
    @property
    def total_count(self):
        """
        The total amount reactions given on the reaction mapping's respective message.
        
        Returns
        -------
        total_count : `int`
        """
        count = 0
        for line in self.values():
            count += set.__len__(line)
            count += line.unknown
        return count
    
    
    def clear(self):
        """
        Clears the reaction mapping with clearing it's lines.
        """
        for value in self.values():
            value.clear()
        if self.fully_loaded:
            self._full_check()
    
    
    def add(self, emoji, user):
        """
        Adds a user to the reactors.
        
        Parameters
        ----------
        emoji : ``Emoji``
            The reacted emoji.
        user : ``ClientUserBase``
            The reactor user.
        """
        try:
            line = self[emoji]
        except KeyError:
            line = reaction_mapping_line(0)
            self[emoji] = line
        line.add(user)
    
    
    def remove(self, emoji, user):
        """
        Removes a user to the reactors.
        
        Parameters
        ----------
        emoji : ``Emoji``
            The removed reacted emoji.
        user : ``ClientUserBase``
            The removed reactor user.
        """
        try:
            line = self[emoji]
        except KeyError:
            return

        if set.__len__(line):
            try:
                line.remove(user)
            except KeyError:
                pass
            else:
                if set.__len__(line) or line.unknown:
                    return
                del self[emoji]
                return
        
        if line.unknown:
            line.unknown -=1
            if set.__len__(line):
                if line.unknown:
                    return
                self._full_check()
                return
            if line.unknown:
                return
            del self[emoji]
    
    
    def remove_emoji(self, emoji):
        """
        Removes all the users who reacted with the given ``Emoji`` and then returns the stored line.
        
        Parameters
        ----------
        emoji : ``Emoji``
            The emoji to remove.
        
        Returns
        -------
        line : `None` or ``reaction_mapping_line``
        """
        line = self.pop(emoji, None)
        if line is None:
            return
        
        if line.unknown:
            self._full_check()
        
        return line
    
    
    # this function is called if an emoji loses all it's unknown reactors
    def _full_check(self):
        """
        Checks whether the reaction mapping is fully loaded, by checking it's values' `.unknown` and sets the current
        state to `.fully_loaded`.
        """
        for line in self.values():
            if line.unknown:
                self.fully_loaded = False
                return
        
        self.fully_loaded = True
    
    
    # we call this when we get SOME reactors of an emoji
    def _update_some_users(self, emoji, users):
        """
        Called when some reactors of an emoji are updated.
        
        Parameters
        ----------
        emoji : ``Emoji``
            The emoji, which's users' are updated.
        users : `list` of ``ClientUserBase``
            The added reactors.
        """
        self[emoji].update(users)
        self._full_check()
        
    def _update_all_users(self, emoji, users):
        """
        Called when all the reactors of an emoji are updated of the reaction mapping.
        
        Parameters
        ----------
        emoji : ``Emoji``
            The emoji, which's users' are updated.
        users : `list` of ``ClientUserBase``
            The added reactors.
        """
        self[emoji] = reaction_mapping_line._full(users)
        self._full_check()


class reaction_mapping_line(set):
    """
    A `set` subclass which contains the users who reacted with the given ``Emoji`` on a ``Message``.
    
    Attributes
    ----------
    unknown : `int`
        The amount of not known reactors.
    """
    __slots__ = ('unknown',)
    
    def __init__(self, unknown):
        """
        Creates a `reaction_mapping_line`.
        
        Parameters
        ----------
        unknown : `int`
            The amount of not known reactors.
        """
        self.unknown = unknown
    
    def __len__(self):
        """Returns the amount of users, who reacted with the given emoji on the respective message."""
        return set.__len__(self)+self.unknown
    
    
    def __repr__(self):
        """Returns the representation of the container."""
        repr_parts = [
            self.__class__.__name__,
            '({',
        ]
        
        # set indexing is not public, so we need to do a check, like this
        if set.__len__(self):
            for user in self:
                repr_parts.append(repr(user))
                repr_parts.append(', ')
            
            repr_parts[-1] = '}'
        else:
            repr_parts.append('}')
        
        unknown = self.unknown
        if unknown:
            repr_parts.append(', unknown=')
            repr_parts.append(repr(unknown))
        
        repr_parts.append(')')
        
        return ''.join(repr_parts)
    
    
    @classmethod
    def _full(cls, users):
        """
        Creates a new ``reaction_mapping_line`` with the given users with `.unknown` set to `0`.
        
        Parameters
        ----------
        users : `list` of ``ClientUserBase``
            A `list`, which should already contain all the users of the reaction mapping line.

        Returns
        -------
        self : ``reaction_mapping_line``
        """
        self = set.__new__(cls)
        set.__init__(self, users)
        self.unknown = 0
        return self
    
    
    def update(self, users):
        """
        Updates the reaction mapping line with the given users.
        
        Parameters
        ----------
        users : `list` of ``ClientUserBase``
            A `list` of users, who reacted on the respective `Message` with the respective ``Emoji``.
        """
        ln_old = len(self)
        set.update(self,users)
        ln_new = len(self)
        self.unknown -= (ln_new-ln_old)
    
    
    def copy(self):
        """
        Copies the reaction mapping line.
        
        Returns
        -------
        new : ``reaction_mapping_line``
        """
        new = set.__new__(type(self))
        set.__init__(new,self)
        new.unknown = self.unknown
        return new
    
    
    # executes an api request if we know we know all reactors
    def filter_after(self, limit, after):
        """
        If we know all the reactors, then instead of executing a Discord API request we filter the reactors locally
        using this method.
        
        Parameters
        ----------
        limit : `int`
            The maximal limit of the users to return.
        after : `int`
            Gets the users after this specified id.
        
        Returns
        -------
        users : `
        """
        list_form = sorted(self)
        
        after = after+1 # do not include the specified id
        
        bot = 0
        top = len(list_form)
        while True:
            if bot < top:
                half = (bot+top)>>1
                if list_form[half].id < after:
                    bot = half+1
                else:
                    top = half
                continue
            break
        
        index = bot
        
        length = len(list_form)
        users = []
        
        while True:
            if index == length:
                break
            
            if limit <= 0:
                break
            
            users.append(list_form[index])
            index += 1
            limit -= 1
            continue
        
        return users
    
    
    def clear(self):
        """
        Clears the reaction mapping line by removing every ``User`` object from it.
        """
        clients = []
        for user in self:
            if isinstance(user, Client):
                clients.append(user)

        self.unknown += (set.__len__(self) - len(clients))
        set.clear(self)
        set.update(self,clients)
