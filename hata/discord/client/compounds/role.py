__all__ = ()

import warnings

from scarletio import Compound, Theory, change_on_switch

from ...bases import maybe_snowflake_pair
from ...core import GUILDS, ROLES
from ...emoji import Emoji
from ...guild import create_partial_guild_from_id
from ...http import DiscordHTTPClient
from ...payload_building import build_create_payload, build_edit_payload
from ...role import Role
from ...role.role.utils import ROLE_FIELD_CONVERTERS

from ..functionality_helpers import role_move_key, role_reorder_valid_roles_sort_key
from ..request_helpers import get_guild_and_id, get_guild_id, get_role_role_guild_id_and_id, get_role_guild_id_and_id


class ClientCompoundRoleEndpoints(Compound):
    
    http : DiscordHTTPClient
    
    @Theory
    async def guild_sync(self, guild): ...
    
    
    async def guild_role_get_all(self, guild):
        """
        Requests the given guild's roles and if there any de-sync between the wrapper and Discord, applies the
        changes.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's roles will be requested.
        
        Returns
        -------
        roles : `list` of ``Role``
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild``, nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild, guild_id = get_guild_and_id(guild)
        
        data = await self.http.guild_role_get_all(guild_id)
        if guild is None:
            guild = create_partial_guild_from_id(guild_id)
        
        guild._update_roles(data)
        
        return [*guild.roles.values()]
    
    
    async def role_create(self, guild, role_template = None, *, reason = None, icon = ..., **keyword_parameters):
        """
        Creates a role at the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild where the role will be created.
        
        role_template : `None`, ``Role`` = `None`, Optional
            Role entity to use as a template.
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the guild's audit logs.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters to create the role with.
        
        Other Parameters
        ----------------
        color : ``Color``, `int`, Optional (Keyword only)
            The role's color.
        
        flags : ``RoleFlag``, `int`, Optional (Keyword only)
            The role's flags.
        
        icon : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The role's icon.
        
        mentionable : `bool`, Optional (Keyword only)
            Whether the role can be mentioned.
        
        name : `str`, Optional (Keyword only)
            The role's name.
        
        permissions : `int`, ``Permission``, Optional (Keyword only)
            The permissions of the users having the role.
        
        position : `int`, Optional (Keyword only)
            The role's position.
        
        separated : `bool`, Optional (Keyword only)
            Users show up in separated groups by their highest `separated` role.
        
        unicode_emoji : `None`, ``Emoji``, Optional (Keyword only)
            The role's icon as an unicode emoji.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        
        # checkout icon
        if (icon is not ...):
            if isinstance(icon, Emoji):
                warnings.warn(
                    (
                        f'Passing `icon` parameters as `{Emoji.__name__}` into `{self.__class__.__name__}.role_create` '
                        f'Is deprecated and will be removed in 2023 February. '
                        f'Please use the `unicode_emoji` parameter instead.'
                    ),
                    FutureWarning,
                    stacklevel = 2,
                )
                
                icon_key = 'unicode_emoji'
                
            else:
                icon_key = 'icon'
            
            keyword_parameters[icon_key] = icon
        
        data = build_create_payload(role_template, ROLE_FIELD_CONVERTERS, keyword_parameters)
        role_data = await self.http.role_create(guild_id, data, reason)
        
        return Role.from_data(role_data, guild_id)
    
    
    async def role_edit(self, role, role_template = None, *, icon = ..., reason = None, **keyword_parameters):
        """
        Edits the role with the given parameters.
        
        This method is a coroutine.
        
        Parameters
        ----------
        role : ``Role``, `tuple` (`int`, `int`)
            The role to edit.
        
        role_template : `None`, ``Role`` = `None`, Optional
            Role entity to use as a template.
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the guild's audit logs.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters to edit the role with.
        
        Other Parameters
        ----------------
        color : ``Color``, `int`, Optional (Keyword only)
            The role's color.
        
        flags : ``RoleFlag``, `int`, Optional (Keyword only)
            The role's flags.
        
        icon : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The role's icon.
            
        mentionable : `bool`, Optional (Keyword only)
            Whether the role can be mentioned.
        
        name : `str`, Optional (Keyword only)
            The role's name.
        
        permissions : `int`, ``Permission``, Optional (Keyword only)
            The permissions of the users having the role.
        
        position : `int`, Optional (Keyword only)
            The role's position.
        
        separated : `bool`, Optional (Keyword only)
            Users show up in separated groups by their highest `separated` role.
        
        unicode_emoji : `None`, ``Emoji``, Optional (Keyword only)
            The role's icon as an unicode emoji.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        role, guild_id, role_id = get_role_role_guild_id_and_id(role)
        
        # checkout icon
        if (icon is not ...):
            if isinstance(icon, Emoji):
                warnings.warn(
                    (
                        f'Passing `icon` parameters as `{Emoji.__name__}` into `{self.__class__.__name__}.role_create` '
                        f'Is deprecated and will be removed in 2023 February. '
                        f'Please use the `unicode_emoji` parameter instead.'
                    ),
                    FutureWarning,
                    stacklevel = 2,
                )
                
                icon_key = 'unicode_emoji'
                
            else:
                icon_key = 'icon'
            
            keyword_parameters[icon_key] = icon
        
        
        data = build_edit_payload(role, role_template, ROLE_FIELD_CONVERTERS, keyword_parameters)
        
        if data:
            await self.http.role_edit(guild_id, role_id, data, reason)
    
    
    async def role_delete(self, role, *, reason = None):
        """
        Deletes the given role.
        
        This method is a coroutine.
        
        Parameters
        ----------
        role : ``Role``, `tuple` (`int`, `int`)
            The role to delete
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            If `role` was not given neither as ``Role`` nor as `tuple` of (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id, role_id = get_role_guild_id_and_id(role)
        await self.http.role_delete(guild_id, role_id, reason)
    
    
    async def role_move(self, role, position, *, reason = None):
        """
        Moves the given role.
        
        This method is a coroutine.
        
        Parameters
        ----------
        role : ``Role``, `tuple` of (`int`, `int`)
            The role to move.
        position : `int`
            The position to move the given role.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            If `role` was not given neither as ``Role`` nor as `tuple` of (`int`, `int`).
        ValueError
            - If default role would be moved.
            - If any role would be moved to position `0`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        if isinstance(role, Role):
            guild_id = role.guild_id
            role_id = role.id
        
        else:
            snowflake_pair = maybe_snowflake_pair(role)
            if snowflake_pair is None:
                raise TypeError(
                    f'`role` can be `{Role.__name__}`, `tuple` (`int`, `int`), got '
                    f'{role.__class__.__name__}; {role!r}.'
                )
            
            guild_id, role_id = snowflake_pair
            role = None
        
        guild = GUILDS.get(guild_id, None)
        if (guild is None) or guild.partial:
            guild = await self.guild_sync(guild_id)
        
        if role is None:
            try:
                role = ROLES[role_id]
            except KeyError:
                # Noice
                return
        
        # Is there nothing to move?
        if role.position == position:
            return
        
        # Default role cannot be moved to position not 0
        if role.position == 0:
            if position != 0:
                raise ValueError(
                    f'Default role cannot be moved, got {role!r}.'
                )
        # non default role cannot be moved to position 0
        else:
            if position == 0:
                raise ValueError(
                    f'Role cannot be moved to position `0`, got {role!r}.'
                )
        
        data = change_on_switch(guild.role_list, role, position, key = role_move_key)
        if not data:
            return
        
        await self.http.role_move(guild_id, data, reason)
    
    
    async def _role_reorder_roles_element_validator(self, item):
        """
        Validates a role-position pair.
        
        This method is a coroutine.
        
        Parameters
        ----------
        item : `tuple` (``Role`` or (`tuple` (`int, `int`), `int`) items or `Any`
            A `dict`, `list`, `set`, `tuple`, which contains role-position items.
        
        Returns
        -------
        role : ``Role``
            The validated role.
        guild : ``None`, ``Guild``
            The role's guild.
        
        Yields
        ------
        item : `None`, `tuple` (``Role``, ``Guild``, `int`)
        
        Raises
        ------
        TypeError
            If `item` has invalid format.
        """
        if not isinstance(item, tuple):
            raise TypeError(
                f'`roles` item can be `tuple`, got {item.__class__.__name__}; {item!r}.'
            )
        
        item_length = len(item)
        if item_length != 2:
            raise TypeError(
                f'`roles` item length can be `2`, got {item_length!r}; {item!r}.'
            )
        
        role, position = item
        if isinstance(role, Role):
            guild_id = role.guild_id
            role_id = role.id
        
        else:
            snowflake_pair = maybe_snowflake_pair(role)
            if snowflake_pair is None:
                raise TypeError(
                    f'`roles` item[0] can be `{Role.__name__}`, `tuple` (`int`, `int`), got '
                    f'{role.__class__.__name__}; {role!r}.'
                )
            
            guild_id, role_id = snowflake_pair
            role = None
        
        guild = GUILDS.get(guild_id, None)
        if (guild is None) or guild.partial:
            guild = await self.guild_sync(guild_id)
        
        if role is None:
            role = ROLES.get(role_id, None)
        
        if not isinstance(position, int):
            raise TypeError(
                f'`position` can be `int`, got {position.__class__.__name__}; {position!r}.'
            )
        
        return role, guild, position
    
    
    async def _role_reorder_roles_validator(self, roles):
        """
        Validates `roles` parameter of ``.role_reorder``.
        
        This method is an asynchronous generator.
        
        Parameters
        ----------
        roles : (`dict` like or `iterable`) of `tuple` (``Role`` or (`tuple` (`int, `int`), `int`) items
            A `dict`, `list`, `set`, `tuple`, which contains role-position items.
        
        Yields
        ------
        item : `None`, `tuple` (``Role``, ``Guild``, `int`)
        
        Raises
        ------
        TypeError
            If `roles`'s format is not any of the expected ones.
        """
        if isinstance(roles, dict):
            for item in roles.items():
                yield await self._role_reorder_roles_element_validator(item)
        elif isinstance(roles, (list, set, tuple)):
            for item in roles:
                yield await self._role_reorder_roles_element_validator(item)
        else:
            raise TypeError(
                f'`roles` can be `dict-like` with (`{Role.__name__}, `int`) items, or as other '
                f'iterable with (`{Role.__name__}, `int`) elements, got {roles!r}.'
            )
    
    
    async def role_reorder(self, roles, *, reason = None):
        """
        Moves more roles at their guild to the specific positions.
        
        Partial roles are ignored and if passed any, every role's position after it is reduced. If there are roles
        passed with different guilds, then `ValueError` will be raised. If there are roles passed with the same
        position, then their positions will be sorted out.
        
        This method is a coroutine.
        
        Parameters
        ----------
        roles : (`dict` like or `iterable`) of `tuple` (``Role`` or (`tuple` (`int`, `int`), `int`) items
            A `dict`, `list`, `set`, `tuple`, which contains role-position items.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            If `roles`'s format is not any of the expected ones.
        ValueError
            - If default role would be moved.
            - If any role would be moved to position `0`.
            - If roles from more guilds are passed.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        # Lets check `roles` structure
        roles_valid = []
        
        guild = None
        
        # Is `roles` passed as dict-like?
        async for element in self._role_reorder_roles_validator(roles):
            if element is None:
                continue
            
            role, maybe_guild, position = element
            if maybe_guild is None:
                pass
            if guild is None:
                guild = maybe_guild
            else:
                if guild is not maybe_guild:
                    raise ValueError(
                        f'`roles` are from multiple guilds, got {roles!r}; guild_1={guild!r}; '
                        f'guild_2={guild!r}.'
                    )
            
            roles_valid.append((role, position))
        
        # Nothing to move, nice
        if not roles_valid:
            return
        
        # Check default and moving to default position
        index = 0
        limit = len(roles_valid)
        while True:
            if index == limit:
                break
            
            role, position = roles_valid[index]
            # Default role cannot be moved
            if (role is not None) and (role.position == 0):
                if position != 0:
                    raise ValueError(
                        f'Default role cannot be moved, got {role!r}; roles={roles!r}.'
                    )
                
                # default and moving to default, lets delete it
                del roles_valid[index]
                limit -= 1
                continue
                
            else:
                # Role cannot be moved to default position
                if position == 0:
                    raise ValueError(
                        f'Role cannot be moved to position `0`, got {role!r}; roles={roles!r}.'
                    )
            
            index += 1
            continue
        
        if not limit:
            return
        
        # Check dupe roles
        roles = set()
        ln = 0
        
        for role, position in roles_valid:
            if role is None:
                continue
            
            roles.add(role)
            if len(roles) == ln:
                raise ValueError(
                    f'`{Role.__name__}`: {role!r} is duped, got {roles!r}.'
                )
            
            ln += 1
            continue
        
        # Now that we have the roles, lets order them
        roles_valid.sort(key = role_reorder_valid_roles_sort_key)
        
        # Cut out non roles.
        limit = len(roles_valid)
        index = 0
        negate_position = 0
        while (index < limit):
            role, position = roles_valid[index]
            if role is None:
                del roles_valid[-1]
                limit -= 1
                negate_position += 1
            else:
                
                if negate_position:
                    roles_valid[index] = (role, position - negate_position)
                
                index += 1
        
        # Remove dupe indexes
        index = 0
        limit = len(roles_valid)
        last_position = 0
        increase_position = 0
        while (index < limit):
            role, position = roles_valid[index]
            if position == last_position:
                increase_position += 1
            
            if increase_position:
                roles_valid[index] = (role, position + increase_position)
            
            last_position = position
            index += 1
            continue
        
        
        # Lets cut out every other role from the guild's
        roles_leftover = set(guild.roles.values())
        for item in roles_valid:
            role = item[0]
            roles_leftover.remove(role)
        
        roles_leftover = sorted(roles_leftover)
    
        target_order = []
        
        index_valid = 0
        index_leftover = 0
        limit_valid = len(roles_valid)
        limit_leftover = len(roles_leftover)
        position_target = 0
        
        while True:
            if index_valid == limit_valid:
                while True:
                    if index_leftover == limit_leftover:
                        break
                    
                    role = roles_leftover[index_leftover]
                    index_leftover += 1
                    target_order.append(role)
                    continue
                
                break
            
            if index_leftover == limit_leftover:
                while True:
                    if index_valid == limit_valid:
                        break
                    
                    role = roles_valid[index_valid][0]
                    index_valid += 1
                    target_order.append(role)
                    continue
                
                
                break
            
            role, position = roles_valid[index_valid]
            if position == position_target:
                position_target += 1
                index_valid += 1
                target_order.append(role)
                continue
            
            role = roles_leftover[index_leftover]
            position_target = position_target + 1
            index_leftover = index_leftover + 1
            target_order.append(role)
            continue
        
        data = []
        
        for index, role in enumerate(target_order):
            position = role.position
            if index == position:
                continue
            
            data.append(role_move_key(role, index))
            continue
        
        # Nothing to move
        if not data:
            return
        
        await self.http.role_move(guild.id, data, reason)
