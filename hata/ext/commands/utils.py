# -*- coding: utf-8 -*-
__all__ = ('Cooldown', )

from ...backend.event_loop import LOOP_TIME
from ...discord.client_core import KOKORO
from ...discord.message import Message

from .command import CommandWrapper


class _CDUnit:
    """
    A cooldown unit stored by a ``CooldownWrapper``.
    
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
        Creates a new ``_CDUnit`` with the given parameters.
        
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

class CooldownWrapper(CommandWrapper):
    """
    Rich command wrapper of ``Cooldown``. Check ``CommandWrapper`` itself for more details.
    
    This subclass adds `Cooldown.shared` feature to the command wrappers created by ``Cooldown``.
    """
    __slots__ = ()
    def shared(self, weight=0, func=None):
        """
        Creates a new cooldown instance, which cooldown is shared with the source one.
        
        Parameters
        ----------
        weight : `int`, Optional
            The weight of one call. Defaults to `1`.
        func : `async-callable`, Optional
            The wrapped command. If not given, returns a wrapper, what can be used as a decorator.

        Returns
        -------
        wrapper : ``Cooldown._wrapper`` or ``CooldownWrapper``
            If `func` is given, then returns the created ``CooldownWrapper``, if not, then returns a wrapper,
            what can be used as a decorator.
        
        Raises
        ------
        TypeError
            If `weight` is not numeric convertable to `int`.
        """
        weight_type = weight.__class__
        if weight_type is int:
            pass
        elif issubclass(weight_type, int):
            weight = int(weight)
        else:
            raise TypeError(f'`weight` can be given as `int` instance, got {weight_type.__name__}.') from None
        
        source_wrapper = self.wrapper
        if weight == 0:
            weight = source_wrapper.weight
        
        new_wrapper = object.__new__(type(source_wrapper))
        new_wrapper.checker = source_wrapper.checker
        new_wrapper.reset = source_wrapper.reset
        new_wrapper.cache = source_wrapper.cache
        new_wrapper.weight = weight
        new_wrapper.limit = source_wrapper.limit+source_wrapper.weight-weight
        
        if func is None:
            wrapper = source_wrapper._wrapper(new_wrapper, self.handler)
        else:
            wrapper = CooldownWrapper(func, new_wrapper, self.handler)
        
        return wrapper

class Cooldown:
    """
    Helper class for implement cooldowns.
    
    > Rework planned.
    
    Examples
    --------
    
    **Using a cooldown handler example:**
    
    ```py
    from hata import DiscordException, CancelledError, sleep, ERROR_CODES, KOKORO
    from hata.ext.commands import Cooldown
    
    class CooldownHandler:
        __slots__ = ('cache',)
        
        def __init__(self):
            self.cache = {}
        
        async def __call__(self, client, message, command, time_left):
            user_id = message.author.id
            try:
                notification,waiter = self.cache[user_id]
            except KeyError:
                pass
            else:
                if notification.channel is message.channel:
                    try:
                        await client.message_edit(notification,
                            f'**{message.author:f}** please cool down, {time_left:.0f} seconds left!')
                    except BaseException as err:
                        if isinstance(err, ConnectionError):
                            return
                        
                        if isinstance(err, DiscordException):
                            if err.code in (
                                    ERROR_CODES.unknown_message, # message deleted
                                    ERROR_CODES.unknown_channel, # channel deleted
                                    ERROR_CODES.invalid_access, # client removed
                                        ):
                                return
                        
                        await client.events.error(client, f'{self!r}.__call__', err)
                    
                    return
                
                waiter.cancel()
            
            try:
                notification = await client.message_create(message.channel,
                    f'**{message.author:f}** please cool down, {time_left:.0f} seconds left!')
            except BaseException as err:
                if isinstance(err, ConnectionError):
                    return
                
                if isinstance(err, DiscordException):
                    if err.code in (
                            ERROR_CODES.unknown_message, # message deleted
                            ERROR_CODES.unknown_channel, # message's channel deleted
                            ERROR_CODES.invalid_access, # client removed
                            ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                            ERROR_CODES.cannot_message_user, # user has dm-s disallowed
                                ):
                        return
                
                await client.events.error(client, f'{self!r}.__call__', err)
            
            waiter = Task(self.waiter(client, user_id, notification), KOKORO)
            self.cache[user_id] = (notification, waiter)
        
        async def waiter(self, client, user_id, notification):
            try:
                await sleep(30., KOKORO)
            except CancelledError:
                pass
            
            del self.cache[user_id]
            
            try:
                await client.message_delete(notification)
            except BaseException as err:
                if isinstance(err, ConnectionError):
                    # no internet
                    return
                
                if isinstance(err, DiscordException):
                    if err.code in (
                            ERROR_CODES.unknown_channel, # message's channel deleted
                            ERROR_CODES.unknown_message, # message deleted
                            ERROR_CODES.invalid_access, # client removed
                                ):
                        return
                
                await client.events.error(client, f'{self!r}.__call__', err)
    
    @Bot.commands
    @Cooldown('user', 30., handler=CooldownHandler())
    async def ping(client, message):
        await client.message_create(message.channel, f'{client.gateway.latency.:.0f} ms')
    ```
    
    **Using shared cooldowns:**

    ```py
    from hata import Embed
    from hata.ext.commands import Converter, ConverterFlag
    
    @Bot.commands
    @Cooldown('user', 60., limit=3, weight=2, handler=CooldownHandler())
    async def avatar(client, message, user : Converter('user', flags=ConverterFlag.user_default.update_by_keys(everywhere=True), default_code='message.author')):
        url = user.avatar_url_as(size=4096)
        embed = Embed(f'{user:f}\'s avatar', url=url)
        embed.add_image(url)
        await client.message_create(message.channel, embed=embed)
    
    @Bot.commands
    @avatar.shared(weight=1)
    async def myavatar(client, message):
        url = message.author.avatar_url_as(size=4096)
        embed = Embed('Your avatar', url=url)
        embed.add_image(url)
        await client.message_create(message.channel, embed=embed)
    ```
    
    Attributes
    ----------
    cache : `dict` of (``DiscordEntity``, ``_CDUnit``) items
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
    
    def __new__(cls, for_, reset, limit=1, weight=1, handler=None, func=None):
        """
        Creates a new
        
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
        handler : `None` or `async-callable`
            Called, when the wrapped command is on cooldown.
            
            If given then 4 parameters will be passed to it:
            +-------------------+---------------+
            | Respective name   | Type          |
            +===================+===============+
            | client            | ``Client``    |
            +-------------------+---------------+
            | message           | ``Message``   |
            +-------------------+---------------+
            | command           | ``Command``   |
            +-------------------+---------------+
            | time_left         | `float`       |
            +-------------------+---------------+
        
        func : `async-callable`, Optional
            The wrapped command. If not given, returns a wrapper, what can be used as a decorator.
        
        Returns
        -------
        wrapper : ``Cooldown._wrapper`` / ``CooldownWrapper``
            If `func` is given, then returns the created ``CooldownWrapper``, if not, then returns a wrapper,
            what can be used as a decorator.
        
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
        for_type = for_.__class__
        if for_type is str:
            pass
        elif issubclass(for_, str):
            for_ = str(for_)
        else:
            raise TypeError(f'`for_` can be given as `str` instance, got {for_type.__name__}.')
    
        if 'user'.startswith(for_):
            checker = cls._check_user
        elif 'channel'.startswith(for_):
            checker = cls._check_channel
        elif 'guild'.startswith(for_):
            checker = cls._check_guild
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
        
        if func is None:
            wrapper = self._wrapper(self, handler)
        else:
            wrapper = CooldownWrapper(func, self, handler)
        
        return wrapper
    
    class _wrapper:
        """
        When a parent ``Command`` instance would be created without giving `func` parameter, then a wrapper of this
        type is returned enabling using ``Cooldown` as a decorator, with still giving parameters to it.
        
        Attributes
        ----------
        parent : ``Cooldown``
            The parent cooldown instance.
        handler : `None` or `async-callable`
            Called, when the wrapped command is on cooldown.
            
            If given then 4 parameters will be passed to it:
            +-------------------+---------------+
            | Respective name   | Type          |
            +===================+===============+
            | client            | ``Client``    |
            +-------------------+---------------+
            | message           | ``Message``   |
            +-------------------+---------------+
            | command           | ``Command``   |
            +-------------------+---------------+
            | time_left         | `float`       |
            +-------------------+---------------+
        """
        __slots__ = ('parent', 'handler')
        def __init__(self, parent, handler):
            """
            Creates a new ``Cooldown._wrapper`` instance with the given parameters.
            
            Parameters
            ----------
            parent : ``Cooldown``
                The parent cooldown instance.
            handler : `None` or `async-callable`
                Called, when the wrapped command is on cooldown.
                
                If given then 4 parameters will be passed to it:
                +-------------------+---------------+
                | Respective name   | Type          |
                +===================+===============+
                | client            | ``Client``    |
                +-------------------+---------------+
                | message           | ``Message``   |
                +-------------------+---------------+
                | command           | ``Command``   |
                +-------------------+---------------+
                | time_left         | `float`       |
                +-------------------+---------------+
            """
            self.parent = parent
            self.handler = handler
        
        def __call__(self, func):
            """
            By calling a cooldown's ``._wrapper`` a ``CooldownWrapper`` instance is created and returned, what can be
            added as a command.
            
            Parameters
            ----------
            func : `async-callable`
                The wrapped function by the cooldown to add as a command.

            Returns
            -------
            wrapper : ``CooldownWrapper``
            """
            if func is None:
                raise TypeError('`func` is given as `None`.')
            
            return CooldownWrapper(func, self.parent, self.handler)
    
    async def __call__(self, client, message):
        """
        Calls the cooldown with the respective `client` and `message`, and then yields whether the command can be
        called, and if not, then with what extra parameters the handler should receive.
        
        This method is a coroutine generator.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the respective message.
        message : ``Message``
            The received message.
        
        Yields
        ------
        passed : `bool`
            Whether the command can be called. If not, then yields additional parameters to call the cooldown's
            handler with.
        time_left : `float`
            How much time is left till the cooldown's expiration.
        """
        value = self.checker(self, message)
        if not value:
            yield True
            return
        
        yield False
        yield value-LOOP_TIME()
        return
    
    @staticmethod
    def _check_user(self, message):
        """
        Executes user cooldown check.
        
        Might be set as the ``Cooldown``'s ``.checker`` instance attribute.
        
        Parameters
        ----------
        message : ``Message``
            The received message.
        
        Returns
        -------
        expires_at : `int`
            When the cooldown for the given entity will expire.
        """
        id_ = message.author.id
        
        cache = self.cache
        try:
            unit = cache[id_]
        except KeyError:
            at_ = LOOP_TIME()+self.reset
            cache[id_] = _CDUnit(at_, self.limit)
            KOKORO.call_at(at_, dict.__delitem__, cache, id_)
            return 0.
        
        left = unit.uses_left
        if left > 0:
            unit.uses_left = left-self.weight
            return 0.
        return unit.expires_at
    
    @staticmethod
    def _check_channel(self, message):
        """
        Executes channel cooldown check.
        
        Might be set as the ``Cooldown``'s ``.checker`` instance attribute.
        
        Parameters
        ----------
        message : ``Message``
            The received message.
        
        Returns
        -------
        expires_at : `int`
            When the cooldown for the given entity will expire.
        """
        id_ = message.channel.id
        
        cache = self.cache
        try:
            unit = cache[id_]
        except KeyError:
            at_ = LOOP_TIME()+self.reset
            cache[id_] = _CDUnit(at_, self.limit)
            KOKORO.call_at(at_, dict.__delitem__, cache, id_)
            return 0.
        
        left = unit.uses_left
        if left>0:
            unit.uses_left = left-self.weight
            return 0.
        return unit.expires_at
    
    #returns -1. if non guild
    @staticmethod
    def _check_guild(self, message):
        """
        Executes guild based cooldown check.
        
        Might be set as the ``Cooldown``'s ``.checker`` instance attribute.
        
        Parameters
        ----------
        message : ``Message``
            The received message.
        
        Returns
        -------
        expires_at : `int`
            When the cooldown for the given entity will expire.
            
            If the cooldown limitation is not applicable for the given entity, returns `-1.0`.
        """
        channel = message.channel
        if channel.type in (1, 3):
            return -1.
        else:
            id_ = channel.guild.id
        
        cache = self.cache
        try:
            unit = cache[id_]
        except KeyError:
            at_ = LOOP_TIME()+self.reset
            cache[id_] = _CDUnit(at_,self.limit)
            KOKORO.call_at(at_, dict.__delitem__, cache, id_)
            return 0.
        
        left = unit.uses_left
        if left > 0:
            unit.uses_left = left-self.weight
            return 0.
        return unit.expires_at
