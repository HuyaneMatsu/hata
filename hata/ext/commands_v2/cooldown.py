__all__ = ('CooldownHandler', )

from ...backend.event_loop import LOOP_TIME

from ...discord.channel import ChannelGuildBase
from ...discord.core import KOKORO

from .exceptions import CommandCooldownError

class CooldownUnit:
    """
    A cooldown unit stored by a ``CommandCooldownWrapper``-s.
    
    Attributes
    ----------
    expires_at : `float`
        When the cooldown unit will expire in LOOP_TIME time.
    uses_left : `int`
        How much uses are left till the respective entity will be locked by cooldown.
    """
    __slots__ = ('expires_at', 'uses_left',)
    def __init__(self, expires_at, uses_left):
        """
        Creates a new ``CooldownUnit`` with the given parameters.
        
        Parameters
        ----------
        expires_at : `float`
            When the cooldown unit will expire in LOOP_TIME time.
        uses_left : `int`
            How much uses are left till the respective entity will be locked by cooldown.
        """
        self.expires_at = expires_at
        self.uses_left = uses_left
    
    def __repr__(self):
        """Returns the object's representation."""
        return f'{self.__class__.__name__}(expires_at={self.expires_at}, uses_left={self.uses_left})'


def _check_user(cooldown_handler, command_context):
    """
    Executes user cooldown check.
    
    Might be set as the ``Cooldown``'s ``.checker`` instance attribute.
    
    Parameters
    ----------
    cooldown_handler : ``CooldownHandler``
        The parent cooldown handler.
    command_context : ``CommandHandler``
        The received command's context.
    
    Returns
    -------
    expires_at : `int`
        When the cooldown for the given entity will expire.
    """
    user_id = command_context.message.author.id
    
    cache = cooldown_handler.cache
    try:
        unit = cache[user_id]
    except KeyError:
        at_ = LOOP_TIME()+cooldown_handler.reset
        cache[user_id] = CooldownUnit(at_, cooldown_handler.limit)
        KOKORO.call_at(at_, dict.__delitem__, cache, user_id)
        return 0.
    
    left = unit.uses_left
    if left > 0:
        unit.uses_left = left-cooldown_handler.weight
        return 0.
    
    return unit.expires_at


def _check_channel(cooldown_handler, command_context):
    """
    Executes channel cooldown check.
    
    Might be set as the ``Cooldown``'s ``.checker`` instance attribute.
    
    Parameters
    ----------
    cooldown_handler : ``CooldownHandler``
        The parent cooldown handler.
    command_context : ``CommandHandler``
        The received command's context.
    
    Returns
    -------
    expires_at : `int`
        When the cooldown for the given entity will expire.
    """
    channel_id =command_context. message.channel.id
    
    cache = cooldown_handler.cache
    try:
        unit = cache[channel_id]
    except KeyError:
        at_ = LOOP_TIME()+cooldown_handler.reset
        cache[channel_id] = CooldownUnit(at_, cooldown_handler.limit)
        KOKORO.call_at(at_, dict.__delitem__, cache, channel_id)
        return 0.
    
    left = unit.uses_left
    if left > 0:
        unit.uses_left = left-cooldown_handler.weight
        return 0.
    
    return unit.expires_at


def _check_guild(cooldown_handler, command_context):
    """
    Executes guild based cooldown check.
    
    Might be set as the ``Cooldown``'s ``.checker`` instance attribute.
    
    Parameters
    ----------
    cooldown_handler : ``CooldownHandler``
        The parent cooldown handler.
    command_context : ``CommandHandler``
        The received command's context.
    
    Returns
    -------
    expires_at : `int`
        When the cooldown for the given entity will expire.
        
        If the cooldown limitation is not applicable for the given entity, returns `-1.0`.
    """
    channel = command_context.message.channel
    if not isinstance(channel, ChannelGuildBase):
        return -1.0
    
    guild_id = channel.guild.id
    
    cache = cooldown_handler.cache
    try:
        unit = cache[guild_id]
    except KeyError:
        at_ = LOOP_TIME()+cooldown_handler.reset
        cache[guild_id] = CooldownUnit(at_, command_context.self.limit)
        KOKORO.call_at(at_, dict.__delitem__, cache, guild_id)
        return 0.
    
    left = unit.uses_left
    if left > 0:
        unit.uses_left = left-cooldown_handler.weight
        return 0.
    
    return unit.expires_at


class CooldownHandler:
    """
    Cooldown for commands.
    
    Attributes
    ----------
    cache : `dict` of (``DiscordEntity``, ``CooldownUnit``) items
        Cache to remember how much use of the given entity are exhausted already.
    checker : `function`
        Checks after how much time the given entity can use again the respective command.
    limit : `int`
        The amount of how much times the command can be called within a set duration before going on cooldown.
    reset : `float`
        The time after the cooldown resets.
    weight : `int`
        The weight of the command.
    """
    __slots__ = ('cache', 'checker', 'limit', 'reset', 'weight',)
    
    def __new__(cls, for_, reset, limit=1, weight=1):
        """
        Creates a new ``CooldownHandler`` instance from the given parameters.
        
        Parameters
        ----------
        for_ : `str`
            By what type of entity the cooldown should limit the command.
            
            Possible values:
             - `'user'`
             - `'channel'`
             - `'guild'`
         
        reset : `float`
            The reset time of the cooldown.
        
        limit : `int`
            The amount of calls after the respective command goes on cooldown.
        
        weight : `int`, Optional
            The weight of one call. Defaults to `1`.
        
        Raises
        ------
        TypeError
            - If `str` is not given as `str` instance.
            - If `weight` is not numeric convertable to `int`.
            - If `reset` is not numeric convertable to `float`.
            - If `limit` is not numeric convertable to `int`.
        ValueError
            - If `for_` is not given as any of the expected value.
        """
        for_type = type(for_)
        if for_type is str:
            pass
        elif issubclass(for_, str):
            for_ = str(for_)
        else:
            raise TypeError(f'`for_` can be given as `str` instance, got {for_type.__name__}.')
        
        if 'user'.startswith(for_):
            checker = _check_user
        elif 'channel'.startswith(for_):
            checker = _check_channel
        elif 'guild'.startswith(for_):
            checker = _check_guild
        else:
            raise ValueError(f'\'for_\' can be \'user\', \'channel\' or \'guild\', got {for_!r}')
        
        reset_type = reset.__class__
        if (reset_type is not float):
            try:
                __float__ = getattr(reset_type, '__float__')
            except AttributeError:
                raise TypeError(f'The given reset is not `float`, neither other numeric convertable to it, got '
                    f'{reset_type.__name__}.') from None
            
            reset = __float__(reset)
            
        limit_type = limit.__class__
        if limit_type is int:
            pass
        elif issubclass(limit_type, int):
            limit = int(limit)
        else:
            raise TypeError(f'`limit` can be given as `int` instance, got {limit_type.__name__}.') from None
        
        weight_type = weight.__class__
        if weight_type is int:
            pass
        elif issubclass(weight_type, int):
            weight = int(weight)
        else:
            raise TypeError(f'`weight` can be given as `int` instance, got {weight_type.__name__}.') from None
        
        self = object.__new__(cls)
        self.checker = checker
        self.reset = reset
        self.weight = weight
        self.limit = limit-weight
        self.cache = {}
        
        return self
    
    
    async def __call__(self, command_context):
        """
        Calls the cooldown with the respective `client` and `message`, and then yields whether the command can be
        called, and if not, then with what extra parameters the handler should receive.
        
        This method is a coroutine.
        
        Parameters
        ----------
        command_context : ``CommandHandler``
            The received command's context.
        
        Raises
        ------
        CommandCooldownError
            If the command is on cooldown, or if guild-bound cooldown was called from non-guild.
        """
        expires_at = self.checker(self, command_context)
        if expires_at:
            if expires_at == -1:
                expires_after = -1
            else:
                expires_after = expires_at-LOOP_TIME()
            
            raise CommandCooldownError(self, expires_after)
