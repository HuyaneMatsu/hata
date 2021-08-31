__all__ = ('CommandContext', )

from ...backend.export import export

from .command_helpers import get_command_category_trace, handle_exception, run_checks
from .exceptions import CommandCheckError
from .responding import process_command_coroutine


@export
class CommandContext(object):
    """
    Represents a command context within the command is invoked.
    
    Attributes
    ----------
    client : ``Client``
        The client who received the message.
    command : ``Command``
        The command to invoke.
    command_category_trace : `None` or `tuple` of ``CommandCategory``
        Trace of command categories till to the command to invoke if applicable.
    command_function : `None` or ``CommandFunction``
        The command's function to run.
    command_keyword_parameters : `dict` of (`str`, `Any`) items
        Keyword parameters to pass to the command function.
    command_positional_parameters : `list` of `Any`
        Positional parameters to pass to the command function.
    content : `str`
        The message's content after prefix.
    message : ``Message``
        The received message.
    parameters : `None` or `dict` of (`str`, `Any`)
        The parsed parameters.
    prefix : `str`
        The matched prefix or the client's prefix for the given respective message.
    """
    __slots__ = ('client', 'command', 'command_category_trace', 'command_function', 'command_keyword_parameters',
        'command_positional_parameters', 'content', 'message', 'parameters', 'prefix')
    
    def __new__(cls, client, message, prefix, content, command):
        """
        Creates a new command context instance.
        
        client : ``Client``
            The client who received the message.
        message : ``Message``
            The received message.
        prefix : `str`
            The matched prefix or the client's prefix for the given respective message.
        content : `str`
            The message's content after prefix.
        command : ``Command``
            The command to invoke.
        """
        self = object.__new__(cls)
        self.client = client
        self.message = message
        self.parameters = None
        self.prefix = prefix
        self.content = content
        self.command = command
        self.command_category_trace = None
        self.command_function = None
        self.command_keyword_parameters = {}
        self.command_positional_parameters = []
        return self
    
    def __repr__(self):
        """Returns the context's representation."""
        return f'<{self.__class__.__name__} client={self.client!r}, message={self.message!r}, command={self.command!r}>'
    
    def __eq__(self, other):
        """Returns whether the two contexts are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.command != other.command:
            return False
        
        if self.message is not other.message:
            return False
        
        if self.client is not other.client:
            return False
        
        return True
    
    def __hash__(self):
        """Returns the hash value of the context."""
        return hash(self.client) ^ hash(self.message) ^ hash(self.command)
    
    # Properties
    
    @property
    def channel(self):
        """
        Returns the message's channel.
        
        Returns
        -------
        channel : ``ChannelBase``
        """
        return self.message.channel
    
    
    @property
    def guild(self):
        """
        Returns the message's guild.
        
        Returns
        -------
        guild : `None` or ``Guild``
        """
        return self.message.guild
    
    
    @property
    def author(self):
        """
        Returns the message's author.
        
        Returns
        -------
        author : ``ClientUserBase``, ``Webhook``, ``WebhookRepr``
        """
        return self.message.author
    
    
    @property
    def voice_state(self):
        """
        Returns the context' user's voice state in the respective guild.
        
        Returns
        -------
        voice_state : `None` or ``VoiceState``
        """
        message = self.message
        guild = message.guild
        if guild is None:
            return None
        
        return guild.voice_states.get(message.author.id, None)
    
    
    @property
    def voice_client(self):
        """
        Returns the voice client in the message's guild if there is any.
        
        Returns
        -------
        voice_client : `None` or ``VoiceClient``
        """
        guild_id = self.message.guild_id
        if guild_id:
            voice_client = self.client.voice_clients.get(guild_id, None)
        else:
            voice_client = None
        
        return voice_client
    
    # API methods
    
    async def reply(self, *args, **kwargs):
        """
        Replies to the command's caller.
        
        This method is a coroutine.
        
        Parameters
        ----------
        content : `str`, ``EmbedBase``, `Any`, Optional
            The message's content if given. If given as `str` or empty string, then no content will be sent, meanwhile
            if any other non `str` or ``EmbedBase`` instance is given, then will be casted to string.
            
            If given as ``EmbedBase`` instance, then is sent as the message's embed.
            
        embed : ``EmbedBase`` instance or `list` of ``EmbedBase`` instances, Optional (Keyword only)
            The embedded content of the message.
            
            If `embed` and `content` parameters are both given as  ``EmbedBase`` instance, then `TypeError` is raised.
            
            If embeds are given as a list, then the first embed is picked up.
        file : `Any`, Optional (Keyword only)
            A file or files to send. Check ``create_file_form`` for details.
        sticker : `None`, ``Sticker``, `int`, (`list`, `set`, `tuple`) of (``Sticker``, `int`)
            Sticker or stickers to send within the message.
        components : `None`, ``ComponentBase``, (`set`, `list`) of ``ComponentBase``, Optional (Keyword only)
            Components attached to the message.
            
            > `components` do not count towards having any content in the message.
        allowed_mentions : `None`,  `str`, ``UserBase``, ``Role``, `list` of (`str`, ``UserBase``, ``Role`` )
                , Optional (Keyword only)
            Which user or role can the message ping (or everyone). Check ``parse_allowed_mentions`` for details.
        reply_fail_fallback : `bool`, Optional (Keyword only)
            Whether normal message should be sent if the referenced message is deleted. Defaults to `False`.
        tts : `bool`, Optional (Keyword only)
            Whether the message is text-to-speech.
        nonce : `str`, Optional (Keyword only)
            Used for optimistic message sending. Will shop up at the message's data.
        
        Returns
        -------
        message : ``Message`` or `None`
            Returns `None` if there is nothing to send.
        
        Raises
        ------
        TypeError
            - If `embed` was given as `list`, but it contains not only ``EmbedBase`` instances.
            - If `allowed_mentions` contains an element of invalid type.
            - `content` parameter was given as ``EmbedBase`` instance, meanwhile `embed` parameter was given as well.
            - If invalid file type would be sent.
            - If `sticker` was not given neither as `None`, ``Sticker``, `int`, (`list`, `tuple`, `set`) of \
                (``Sticker``, `int).
        ValueError
            - If `allowed_mentions`'s elements' type is correct, but one of their value is invalid.
            - If more than `10` files would be sent.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `tts` was not given as `bool` instance.
            - If `nonce` was not given neither as `None` nor as `str` instance.
            - If `reply_fail_fallback` was not given as `bool` instance.
        """
        return await self.client.message_create(self.message, *args, **kwargs)
        
    
    async def send(self, *args, **kwargs):
        """
        Sends a message to the channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        content : `str`, ``EmbedBase``, `Any`, Optional
            The message's content if given. If given as `str` or empty string, then no content will be sent, meanwhile
            if any other non `str` or ``EmbedBase`` instance is given, then will be casted to string.
            
            If given as ``EmbedBase`` instance, then is sent as the message's embed.
            
        embed : ``EmbedBase`` instance or `list` of ``EmbedBase`` instances, Optional (Keyword only)
            The embedded content of the message.
            
            If `embed` and `content` parameters are both given as  ``EmbedBase`` instance, then `TypeError` is raised.
            
            If embeds are given as a list, then the first embed is picked up.
        file : `Any`, Optional (Keyword only)
            A file or files to send. Check ``create_file_form`` for details.
        sticker : `None`, ``Sticker``, `int`, (`list`, `set`, `tuple`) of (``Sticker``, `int`)
            Sticker or stickers to send within the message.
        components : `None`, ``ComponentBase``, (`set`, `list`) of ``ComponentBase``, Optional (Keyword only)
            Components attached to the message.
            
            > `components` do not count towards having any content in the message.
        allowed_mentions : `None`,  `str`, ``UserBase``, ``Role``, `list` of (`str`, ``UserBase``, ``Role`` )
                , Optional (Keyword only)
            Which user or role can the message ping (or everyone). Check ``parse_allowed_mentions`` for details.
        tts : `bool`, Optional (Keyword only)
            Whether the message is text-to-speech.
        nonce : `str`, Optional (Keyword only)
            Used for optimistic message sending. Will shop up at the message's data.
        
        Returns
        -------
        message : ``Message`` or `None`
            Returns `None` if there is nothing to send.
        
        Raises
        ------
        TypeError
            - If `embed` was given as `list`, but it contains not only ``EmbedBase`` instances.
            - If `allowed_mentions` contains an element of invalid type.
            - `content` parameter was given as ``EmbedBase`` instance, meanwhile `embed` parameter was given as well.
            - If invalid file type would be sent.
            - If `sticker` was not given neither as `None`, ``Sticker``, `int`, (`list`, `tuple`, `set`) of \
                (``Sticker``, `int).
        ValueError
            - If `allowed_mentions`'s elements' type is correct, but one of their value is invalid.
            - If more than `10` files would be sent.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `tts` was not given as `bool` instance.
            - If `nonce` was not given neither as `None` nor as `str` instance.
            - If `reply_fail_fallback` was not given as `bool` instance.
        """
        return await self.client.message_create(self.message.channel, *args, **kwargs)
    
    
    async def typing(self):
        """
        Triggers typing indicator in the channel.
        
        This method is a coroutine.
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``ChannelTextBase`` nor `int` instance.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        The client will be shown up as typing for 8 seconds, or till it sends a message at the respective channel.
        """
        return await self.client.typing(self.channel)
    
    
    def keep_typing(self, *args, **kwargs):
        """
        Returns a context manager which will keep sending typing events at the channel. Can be used to indicate that
        the bot is working.
        
        Parameters
        ----------
        timeout : `float`, Optional
            The maximal duration for the ``Typer`` to keep typing.
        
        Returns
        -------
        typer : ``Typer``
        
        Examples
        --------
        ```py
        with ctx.typing():
            # Do some things
            await ctx.send('Ayaya')
        ```
        """
        return self.client.keep_typing(self.channel, *args, **kwargs)
    
    
    async def invoke(self):
        """
        Invokes the command.
        
        This method is a coroutine.
        
        Returns
        -------
        invoked : `bool`
            Whether the command was successfully invoked.
            
            If unexpected exception occurs, still returns `True`.
        """
        try:
            command_category_trace, command_function, index = get_command_category_trace(self.command, self.content, 0)
            self.command_category_trace = command_category_trace
            self.command_function = command_function
            
            if (command_function is None):
                return
            
            failed_check = await run_checks(self.command._iter_checks(), self)
            if (failed_check is not None):
                raise CommandCheckError(failed_check)
            
            for wrapper in command_function._iter_wrappers():
                await wrapper(self)
            
            parameter_parsing_states = await command_function._content_parser.parse_content(self, index)
            command_positional_parameters = self.command_positional_parameters
            command_keyword_parameters = self.command_keyword_parameters
            for parameter_parsing_state in parameter_parsing_states:
                parameter_parsing_state.get_parser_value(command_positional_parameters, command_keyword_parameters)
            
            await process_command_coroutine(self,
                command_function._function(*command_positional_parameters, **command_keyword_parameters)
            )
            
        except BaseException as err:
            return await handle_exception(self, err)
        
        return True
