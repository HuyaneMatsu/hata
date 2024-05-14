__all__ = ('ReactionMappingLine',)

from scarletio import RichAttributeErrorBaseType

from .fields import validate_count, validate_users


class ReactionMappingLine(RichAttributeErrorBaseType):
    """
    Contains who reaction with a represented reaction.
    
    Attributes
    ----------
    count : `int`
        The total number of users who reacted.
    users : `None | set<ClientUserBase>`
        The known reactors.
    """
    __slots__ = ('count', 'users')
    
    def __new__(cls, *, count = ..., users = ...):
        # count
        if count is ...:
            count = 0
        else:
            count = validate_count(count)
        
        # users
        if users is ...:
            users = None
        else:
            users = validate_users(users)
        
        # postprocess
        if (users is not None) and (len(users) > count):
            count = len(users)
        
        # Construct
        self = object.__new__(cls)
        self.count = count
        self.users = users
        return self
    
    
    def __len__(self):
        """Returns the amount of known users."""
        users = self.users
        if users is None:
            return 0
        
        return len(users)
    
    
    def __iter__(self):
        """Iterates over the known users."""
        users = self.users
        if (users is not None):
            yield from users
    
    
    def __contains__(self, user):
        """Returns whether the given user is in the known ones."""
        users = self.users
        if (users is None):
            return False
        
        return user in users
    
    
    def __repr__(self):
        """Returns the representation of the container."""
        repr_parts = ['<', type(self).__name__]
        
        # count
        repr_parts.append(', count = ')
        repr_parts.append(repr(self.count))
        
        # users
        repr_parts.append(', users = ')
        repr_parts.append(repr(self.users))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two poll results are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # count
        if self.count != other.count:
            return False
        
        # users
        length = len(self)
        if length != len(other) or (length != 0 and self.users != other.users):
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the count's hash."""
        hash_value = 0
        
        # count
        hash_value ^= self.count
        
        # users
        users = self.users
        if (users is not None):
            hash_value ^= len(users) << 4
            for user in users:
                hash_value ^= hash(user)
        
        return hash_value
    
    
    def _merge_with(self, other):
        """
        Merges the poll result with the other one.
        
        Always `other` is right and `other` should be empty.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            Other instance.
        """
        new_count = other.count
        
        self_users = self.users
        other_users = other.users
        if self_users is None:
            if (other_users is not None):
                self_users = other_users.copy()
                self.users = self_users
        
        else:
            if self.count != new_count:
                self_users.clear()
                if (other_users is not None):
                    self_users.update(other_users)
            
            else:
                if (other_users is not None) and (not other_users.issubset(self_users)):
                    self_users.clear()
                    self_users.update(other_users)
            
        self.count = new_count
    
    
    @classmethod
    def _create_empty(cls):
        """
        Creates a new reaction mapping line.
        
        Parameters
        ----------
        count : `int`
            The amount of reactions to create with.
        
        Returns
        -------
        self : instance<cls>
        """
        self = object.__new__(cls)
        self.count = 0
        self.users = None
        return self
    
    
    def copy(self):
        """
        Copies the reaction mapping line.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        
        new.count = self.count
        
        users = self.users
        if (users is not None):
            users = users.copy()
        new.users = users
        
        return new
    
    
    def copy_with(self, *, count = ..., users = ...):
        """
        Copies the reaction mapping line with the given fields.
        
        Parameters
        ----------
        count : `int`, Optional (Keyword only)
            The amount of reactors.
        
        users : `None`, `iterable` of ``ClientUserBase``, Optional (Keyword only)
            The known users.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # count
        if count is ...:
            count = self.count
        else:
            count = validate_count(count)
        
        # users
        if users is ...:
            users = self.users
            if (users is not None):
                users = users.copy()
        else:
            users = validate_users(users)
        
        # post-checks
        if (users is not None) and (len(users) > count):
            count = len(users)
        
        # Construct
        new = object.__new__(type(self))
        new.count = count
        new.users = users
        return new
    
    
    def _add_reaction(self, user):
        """
        Adds a user.
        
        Parameters
        ----------
        user : ``ClientUserBase``
            The user who reacted.
        
        Returns
        -------
        success : `bool`
        """
        users = self.users
        if users is None:
            self.users = {user}
            self.count += 1
            return True
        
        old_length = len(users)
        users.add(user)
        new_length = len(users)
        if old_length == new_length:
            return False
        
        self.count += 1
        return True
    
    
    def _fill_some_reactions(self, some_users):
        """
        Fills out some users.
        
        Parameters
        ----------
        some_users : `list` of ``ClientUserBase``
            The users who reacted.
        """
        users = self.users
        if users is None:
            if some_users:
                users = {*some_users}
                self.users = users
        else:
            users.update(some_users)
        
        # This should not happen
        if (users is not None) and (self.count < len(users)):
            self.count = len(users)
    
    
    def _fill_all_reactions(self, all_users):
        """
        Fills out all users.
        
        Parameters
        ----------
        all_users : `list` of ``ClientUserBase``
            The users who reacted.
        """
        users = self.users
        if users is None:
            if all_users:
                users = {*all_users}
                self.users = users
        else:
            users.clear()
            users.update(all_users)
        
        # This should not happen
        user_count = 0 if users is None else len(users)
        if self.count != user_count:
            self.count = user_count
    
    
    def _remove_reaction(self, user):
        """
        Removes a user.
        
        Parameters
        ----------
        user : ``ClientUserBase``
            The user who removed their reaction.
        
        Returns
        -------
        success : `bool`
        """
        users = self.users
        count = self.count
        
        if users is None:
            if count <= 0:
                return False
            
            self.count = count - 1
            return True
        
        old_length = len(users)
        users.discard(user)
        new_length = len(users)
        if old_length == new_length:
            count = self.count
            if count <= new_length:
                return False
            
            self.count = count - 1
            return True
        
        if count <= 0:
            return False
        
        self.count = count - 1
        return True
    
    
    @property
    def unknown(self):
        """
        Returns the amount of unknown users.
        
        Returns
        -------
        unknown : `int`
        """
        count = self.count
        users = self.users
        if users is None:
            return count
        
        return count - len(users)
    
    
    def filter_after(self, limit, after):
        """
        If we know all the users, then instead of executing a Discord API request we filter the users locally
        using this method.
        
        Parameters
        ----------
        limit : `int`
            The maximal limit of the users to return.
        after : `int`
            Gets the users after this specified id.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        """
        users = self.users
        if users is None:
            return []
        
        filtered_users = [user for user in self if user.id > after]
        filtered_users.sort()
        del filtered_users[limit:]
        return filtered_users
    
    
    def clear(self):
        """
        Clears the reaction mapping line's users.
        """
        users = self.users
        if (users is not None):
            users.clear()
