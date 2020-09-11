﻿# -*- coding: utf-8 -*-
__all__ = ('Application', 'ApplicationExecutable', 'ApplicationSubEntity', 'EULA', 'Team', 'TeamMember', \
    'TeamMembershipState', 'ThirdPartySKU', )

from .bases import DiscordEntity, IconSlot, ICON_TYPE_NONE
from .http import URLS
from .user import ZEROUSER, User
from .client_core import TEAMS, EULAS, APPLICATIONS

class Application(DiscordEntity, immortal=True):
    """
    Represents a Discord application with all of it's spice.
    
    When a ``Client`` is created, it starts it's life with an empty application by defualt. However when the client
    logs in, it's application is requested, but it can be updated by ``Client.update_application_info`` anytime.
    
    Attributes
    ----------
    bot_public : `bool`.
        Whether not only the application's owner can join the application's bot to guilds. Defaults to `False`
    bot_require_code_grant : `bool`
        Whether the application's bot will only join a guild, when completing the full `oauth2` code grant flow.
        Defaults to `False`.
    cover_hash : `int`
        The application's store cover image's hash in `uint128`. If the application is sold at Discord, this image
        will be used at the store.
    cover_type : ``IconType``
        The application's store cover image's type.
    description : `str`
        The description of the application. Defaults to empty string.
    guild_id : `int`
        If the application is a game sold on Discord, this field tells in which guild it is.
        Defaults to `0` if not applicable.
    icon_hash : `int`
        The application's icon's hash as `uint128`.
    icon_type : ``IconType``
        The application's icon's type.
    id : `int`
        The application's id. Defaults to `0`. Meanwhile set as `0`, hashing the application will raise `RuntimeError`.
    name : `str`
        The name of the application. Defaults to empty string.
    owner : ``User``, ``Client`` or ``Team``
        The application's owner. Defaults to `ZEROUSER`.
    primary_sku_id : `int`
        If the application is a game sold on Discord, this field will be the id of the created `Game SKU`.
        Defaults to `0`.
    rpc_origins : `None` or `list` of `str`
        A list of `rpc` origin urls, if `rpc` is enabled. Set as `None` if would be an empty list.
    slug : `str` or `None`
        If this application is a game sold on Discord, this field will be the url slug that links to the store page.
        Defaults to `None`.
    summary : `str`
        if this application is a game sold on Discord, this field will be the summary field for the store page of its
        primary sku. Defautls to empty string.
    verify_key : `str`
        A base64 encoded key for the GameSDK's `GetTicket`. Defaults to empty string.
    developers : `None` or `list` of ``ApplicationSubEntity``
        A list of the application's games' developers. Defaults to `None`.
    hook : `bool`
        Defaults to `False`.
    publishers : `None` or `list` of ``ApplicationSubEntity``
        A list of the application's games' publishers. Defaults to `None`.
    executables : `None` or `list` of ``ApplicationExecutable``
        A list of the appplication's executables. Defaults to `None`.
    third_party_skus : `None` or `list` of ``ThirdPartySKU``
         A list of the appplication's third party stock keeping units. Defaults to `None`.
    splash_hash : `int`
        The application's splash image's hash as `uint128`.
    splash_type : ``IconType``
        The application's splash image's type.
    overlay : `bool`
        Defaults to `False`.
    overlay_compatibility_hook : `bool`
        Defaults to `False`.
    aliases : `None` or `list` of `str`
        Aliases of the application's name. Defaults to `None`.
    eula_id : `int`
        The end-user license agreement's id of the application. Defaults to `0` if not applicable.
    
    Notes
    -----
    The instances of the class support weakreferencing.
    """
    __slots__ = ('aliases', 'bot_public', 'bot_require_code_grant', 'description', 'developers', 'eula_id',
        'executables', 'guild_id', 'hook', 'name', 'overlay', 'overlay_compatibility_hook', 'owner', 'primary_sku_id',
        'publishers', 'rpc_origins', 'slug', 'summary', 'third_party_skus', 'verify_key', )
    
    cover = IconSlot('cover', 'cover_image', URLS.application_cover_url, URLS.application_cover_url_as, add_updater=False)
    icon = IconSlot('icon', 'icon', URLS.application_icon_url, URLS.application_icon_url_as, add_updater=False)
    splash = IconSlot('splash', 'splash', None, None, add_updater=False)
    
    @classmethod
    def _create_empty(cls):
        """
        Creates an empty application, witth it's defualt attributes set.
        
        Returns
        -------
        self : ``Application``
            The created application
        """
        self = object.__new__(cls)
        
        self.id = 0
        self.name = ''
        self.description = ''
        self.rpc_origins = None
        self.bot_public = False
        self.bot_require_code_grant = False
        self.owner = ZEROUSER
        self.summary = ''
        self.verify_key = ''
        self.guild_id = None
        self.primary_sku_id = 0
        self.slug = None
        self.developers = None
        self.hook = None
        self.publishers = None
        self.executables = None
        self.third_party_skus = None
        self.overlay = False
        self.overlay_compatibility_hook = False
        self.aliases = None
        self.eula_id = 0
        
        self.cover_hash = 0
        self.cover_type = ICON_TYPE_NONE
        self.icon_hash = 0
        self.icon_type = ICON_TYPE_NONE
        self.splash_hash = 0
        self.splash_type = ICON_TYPE_NONE
        
        return self
    
    def _create_update(self, data):
        """
        Cretaes a new application if the given data refers to an other one. Updates the application and returns it.
        
        Parameters
        ----------
        data : or `dict` of (`str`, `Any`) items, Optional
            Application data received from Discord.
        
        Returns
        -------
        self : `˙Application``
            The created or updated application.
        """
        application_id = int(data['id'])
        
        if self.id == 0:
            try:
                self = APPLICATIONS[application_id]
            except KeyError:
                self.id = application_id
                APPLICATIONS[application_id] = self
        
        self._update_no_return(data, set_owner=True)
        
        return self
    
    def __new__(cls, data):
        """
        Creates a new application with the given data. If the application already exists, updates it and returns that
        instead.
        
        Parameters
        ----------
        data : or `dict` of (`str`, `Any`) items, Optional
            Application data received from Discord.
        
        Returns
        -------
        self : `˙Application``
        """
        application_id = int(data['id'])
        try:
            self = APPLICATIONS[application_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = application_id
            self._update_no_return(data, set_owner=True)
        else:
            self._update_no_return(data)
        
        return self
    
    def __hash__(self):
        """Returns the application's hash value."""
        id_ = self.id
        if id_:
            return id_
        
        raise TypeError(f'Cannot hash partial {self.__class__.__name__} object.')
    
    @property
    def partial(self):
        """
        Returns whether the application is partial.
        
        An application if partial, if it's id is set as `0`.
        Returns
        -------
        partial : `bool`
        """
        return (self.id == 0)
    
    def __repr__(self):
        """Returns the application's representation"""
        result = [
            '<',
            self.__class__.__name__,
                ]
        
        id_ = self.id
        if id_:
            result.append(' id=')
            result.append(repr(id_))
            result.append(', name=')
            result.append(repr(self.name))
        else:
            result.append(' partial')
        
        result.append('>')
        
        return ''.join(result)
    
    def __str__(self):
        """Returns the application's name."""
        return self.name
    
    def _update_no_return(self, data, set_owner=False):
        """
        Updates the application with the data received from Discord.
        
        Parameters
        ----------
        data : `None` or `dict` of (`str`, `Any`) items
            Application data received from Discord.
        set_owner : `bool`, Optional
            Whether the application's owner should be set from the given data. Defaults to `False`.
            Should be given as `True`, if the application is created or if it contans owner data.
        """
        self.name = data['name']
        
        self.description = data['description']
        
        rpc_origins = data.get('rpc_origins')
        if (rpc_origins is not None) and (not rpc_origins):
            rpc_origins = None
        
        self.rpc_origins = rpc_origins
        
        self.bot_public = data.get('bot_public', False)
        self.bot_require_code_grant = data.get('bot_require_code_grant', False)
        self.summary = data['summary']
        self.verify_key = data['verify_key']
        
        if set_owner:
            team_data = data.get('team')
            if team_data is None:
                owner_data = data.get('owner')
                if owner_data is None:
                    owner = ZEROUSER
                else:
                    owner = User(owner_data)
            else:
                owner = Team(team_data)
            
            self.owner = owner
        
        guild_id = data.get('guild_id')
        if guild_id is None:
            guild_id = 0
        else:
            guild_id = int(guild_id)
        
        self.guild_id = guild_id
        
        primary_sku_id = data.get('primary_sku_id')
        if primary_sku_id is None:
            primary_sku_id = None
        else:
            primary_sku_id = int(primary_sku_id)
        self.primary_sku_id = primary_sku_id
        
        self.slug = data.get('slug', None)
        
        self._set_cover(data)
        self._set_icon(data)
        
        developers_data = data.get('developers')
        if (developers_data is None) or (not developers_data):
            developers = None
        else:
            developers = [ApplicationSubEntity(developer_data) for developer_data in developers_data]
        
        self.developers = developers
        
        self.hook = data.get('hook', False)
        
        publishers_data = data.get('publishers')
        if (publishers_data is None) or (not publishers_data):
            publishers = None
        else:
            publishers = [ApplicationSubEntity(publisher_data) for publisher_data in publishers_data]
        
        self.publishers = publishers
        
        executables_data = data.get('executables')
        if (executables_data is None) or (not executables_data):
            executables = None
        else:
            executables = [ApplicationExecutable(executable_data) for executable_data in executables_data]
        
        self.executables = executables
        
        self._set_splash(data)
        
        third_party_skus_data = data.get('third_party_skus')
        if (third_party_skus_data is None) or (not third_party_skus_data):
            third_party_skus = None
        else:
            third_party_skus = [ThirdPartySKU(third_party_sku_data) for third_party_sku_data in third_party_skus_data]
        
        self.third_party_skus = third_party_skus
        
        self.overlay = data.get('overlay', False)
        self.overlay_compatibility_hook = data.get('overlay_compatibility_hook', False)
        
        aliases = data.get('aliases')
        if (aliases is not None) and (not aliases):
            aliases = None
        
        self.aliases = aliases
        
        eula_id = data.get('eula_id')
        if eula_id is None:
            eula_id = 0
        else:
            eula_id = int(eula_id)
        
        self.eula_id = eula_id


class Team(DiscordEntity, immortal=True):
    """
    Represents a Team on the Discord developer protal.
    
    Attributes
    ----------
    id : `int`
        The unique identificator number of the team.
    icon_hash : `int`
        The team's icon's hash as `uint128`. Defaults to `0`.
    icon_type : `IconType`
        The team's icon's type.
    members : `list` of `TeamMember`
        The members of the team. Includes invited members as well.
    name : `str`
        The teams name.
    owner : ``User`` or ``Client``
        The team's owner.
    
    Notes
    -----
    Team objects support weakreferencig.
    """
    __slots__ = ('members', 'name', 'owner',)
    
    icon = IconSlot('icon', 'icon', URLS.team_icon_url, URLS.team_icon_url_as, add_updater = False)
    
    def __new__(cls, data):
        """
        Creates a new ``Team`` instance from the data received from Discord.
        
        Parameters
        ----------
        data : `None` or `dict` of (`str`, `Any`) items
            Team data received from Discord.
        
        Returns
        -------
        team : ``Team``
        """
        team_id = int(data['id'])
        try:
            team = TEAMS[team_id]
        except KeyError:
            team = object.__new__(cls)
            team.id = team_id
        
        #update every attribute
        team.name = data['name']
        
        team._set_icon(data)
        
        team.members = members = [TeamMember(team_member_data) for team_member_data in data['members']]
        owner_id = int(data['owner_user_id'])
        
        for member in members:
            user = member.user
            if user.id == owner_id:
                break
        else:
            user = ZEROUSER
        
        team.owner = user
        return team
    
    @property
    def invited(self):
        """
        A list of the invited users to the team.
        
        Returns
        -------
        users : `list` of (``User`` or ``Client``) objects
        """
        target_state = TeamMembershipState.INVITED
        return [team_member.user for team_member in self.members if team_member.state is target_state]
    
    @property
    def accepted(self):
        """
        A list of the users, who accepted their invite to the team.
        
        Returns
        -------
        users : `list` of (``User`` or ``Client``) objects
        """
        target_state = TeamMembershipState.ACCEPTED
        return [team_member.user for team_member in self.members if team_member.state is target_state]
    
    def __str__(self):
        """Returns the team's name."""
        return self.name
    
    def __repr__(self):
        """Returns the team's representation."""
        return f'<{self.__class__.__name__} owner={self.owner.full_name}, total count={len(self.members)}>'

class TeamMember(object):
    """
    Represents a team member of a ``Team``.
    
    Attributes
    ----------
    permissions : `list` of `str`
        The permissions of the team member. Right now specific permissions are not supported, so the list has only
        one element : `'*'`, what represents all the permissions.
    state : ``TeamMembershipState``
        The state of the team member. A member can be invited or can have the invite already accepted.
    user : ``User`` or ``Client``
        The corresponding user account of the team member object.
    """
    __slots__ = ('permissions', 'state', 'user',)
    
    def __init__(self, data):
        """
        Creates a `TeamMember` object from the data sent by Discord.
        
        Parameters
        ----------
        data : `None` or `dict` of (`str`, `Any`) items
            Team member data received from Discord.
        """
        permissions = data['permissions']
        permissions.sort()
        self.permissions = permissions
        self.user = User(data['user'])
        self.state = TeamMembershipState.INSTANCES[data['membership_state']]
    
    def __repr__(self):
        """Returns the team member's representation."""
        return f'<{self.__class__.__name__} user={self.user.full_name} state={self.state.name} permissions={self.permissions}>'
    
    def __hash__(self):
        """Returns the team member's hash value, what is equal to it's user's id."""
        return self.user.id
    
    def __eq__(self, other):
        """Returns whether the two team members are equal."""
        if type(self) is not type(other):
            return False
        
        if (self.user != other.user):
            return False
        
        if (self.state is not other.state):
            return False
        
        if (self.permissions != other.permissions):
            return False
        
        return True

class TeamMembershipState(object):
    """
    Represents a ``TeamMemember``'s state at a ``Team``.
    
    Attributes
    ----------
    name : `str`
        The name of state.
    value : `int`
        The Discord side identificator value of the team membership state.
        
    Class Attributes
    ----------------
    INSTANCES : `list` of ``TeamMembershipState``
        Stores the created team membership state instances. This container is accessed when translating a Discord
        team membership state's value to it's representation.
    
    Every predefined team membership state can be accessed as class attribute as well:
    +-----------------------+-----------+-------+
    | Class attribute name  | name      | value |
    +=======================+===========+=======+
    | NONE                  | NONE      | 0     |
    +-----------------------+-----------+-------+
    | INVITED               | INVITED   | 1     |
    +-----------------------+-----------+-------+
    | ACCEPTED              | ACCEPTED  | 2     |
    +-----------------------+-----------+-------+
    """
    # class related
    INSTANCES = [NotImplemented] * 3
    
    # object related
    __slots__ = ('name', 'value',)
    
    def __init__(self,value,name):
        self.value = value
        self.name = name
        
        self.INSTANCES[value] = self
    
    def __int__(self):
        """Retruns the team membership state's value."""
        return self.value
    
    def __hash__(self):
        """Returns the hash value of the team mebership state, what equals to it's value."""
        return self.value
    
    def __str__(self):
        """Returns the team membership state's name."""
        return self.name
    
    def __repr__(self):
        """Returns the team membership state's representation."""
        return f'{self.__class__.__name__}(value={self.value}, name={self.name!r})'
    
    # predefined
    NONE     = None
    INVITED  = None
    ACCEPTED = None

TeamMembershipState.NONE     = TeamMembershipState(0, 'NONE')
TeamMembershipState.INVITED  = TeamMembershipState(1, 'INVITED')
TeamMembershipState.ACCEPTED = TeamMembershipState(2, 'ACCEPTED')

class ApplicationSubEntity(DiscordEntity):
    """
    An un-typed entity stored inside of an ``Application``, as one of it's `.developers`, or `.publishers`.
    
    Attributes
    ----------
    id : `int`
        The unique identificator number of the entity.
    name : `str`
        The name of the entity.
    """
    __slots__ = ('name', )
    
    def __init__(self, data):
        """
        Creates a new ``ApplicationSubEntity`` instance.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Developers or Publisher data.
        """
        self.id = int(data['id'])
        self.name = data['name']
    
    def __repr__(self):
        """Returns the entity's rerepsentation."""
        return f'<{self.__class__.__name__} {self.name!r}, id={self.id}>'
    
    def __eq__(self, other):
        """Returns whether the two entities equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.id != other.id:
            return False
        
        if self.name != other.name:
            return False
        
        return True

class ApplicationExecutable(object):
    """
    Represents a game's executable.
    
    Attributes
    ----------
    arguments : `None` or `str`
        The arguments to start the application with. Defaults to `None`.
    is_launcher : `bool`
        Whether the application is a launcher. Defaults to `False`.
    name : `str`
        The executable's name.
    os : `str`
        The operation system, the executable is for.
    """
    __slots__ = ('arguments', 'is_launcher', 'name', 'os')
    
    def __init__(self, data):
        """
        Creates a new application executable with the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Executures data.
        """
        self.name = data['name']
        self.os = data['os']
        self.arguments = data.get('arguments')
        self.is_launcher = data.get('is_launcher', False)
    
    def __repr__(self):
        """Returns the executable's representation."""
        result = [
            '<',
            self.__class__.__name__,
            ' ',
            repr(self.name),
            ', os=',
            repr(self.os),
                ]
        
        arguments = self.arguments
        if (arguments is not None):
            result.append(', arguments=')
            result.append(repr(arguments))
        
        is_launcher = self.is_launcher
        if is_launcher:
            result.append(', is_launcher=True')
        
        result.append('>')
        
        return ''.join(result)
    
    def __eq__(self, other):
        """Returns whether the two executables are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.name != other.name:
            return False
        
        if self.os != other.os:
            return False
        
        if self.arguments != other.arguments:
            return False
        
        if self.is_launcher != other.is_launcher:
            return False
        
        return True
    
    def __hash__(self):
        """Returns the entity's hash."""
        result = hash(self.name) ^ hash(self.os)
        
        arguments = self.arguments
        if (arguments is not None):
            result ^= hash(arguments)
        
        if self.is_launcher:
            result ^= (1<<15)
        
        return result

class ThirdPartySKU(object):
    """
    Represents a third party Stock Keeping Unit.
    
    distributor : `str`
        The districbutor of the SKU.
    id : `str`
        The identificator of the third party SKU.
    sku : `str`
        Might be same as `.id`.
    """
    __slots__ = ('distributor', 'id', 'sku',)
    
    def __init__(self, data):
        """
        creates a new third party SKU object from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            SKU data.
        """
        self.distributor = data['distributor']
        self.id = data['id']
        self.sku = data['sku']
    
    def __repr__(self):
        """Returns the SKU's representation."""
        return f'<{self.__class__.__name__} distributor={self.distributor!r}, id={self.id!r}, sku={self.sku!r}>'
    
    def __eq__(self, other):
        """Returns whether the two SKU-s are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.distributor != other.distributor:
            return False
        
        if self.id != other.id:
            return False
        
        if self.sku != other.sku:
            return False
        
        return True
    
    def __hash__(self):
        """Returns the sku's hash."""
        result = hash(self.distributor)
        
        id_ = self.id
        result ^= hash(id_)
        
        sku = self.sku
        if sku != id_:
            result ^= hash(sku)
        
        return result

class EULA(DiscordEntity, immortal=True):
    """
    Represnts a Discord end-user license agreement
    
    Attributes
    ----------
    id : `int`
        The unique identificator number of the eula.
    content : `str`
        The eula's content.
    name : `str`
        The eula's name.
    
    Notes
    -----
    The instances of the class support weakreferencing.
    """
    def __new__(cls, data):
        """
        Creates a new eula instacne from the givne parameters.
        
        If the eula already exists, returns that instead.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Eula data.
        """
        eula_id = int(data['id'])
        
        try:
            self = EULAS[eula_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = eula_id
            self.content = data['content']
            self.name = data['name']
            
            EULAS[eula_id] = self
        
        return self
    
    def __repr__(self):
        """Returns the eula's representation"""
        return f'<{self.__class__.__name__} {self.name!r}, id={self.id}>'

del URLS
del DiscordEntity
del IconSlot
