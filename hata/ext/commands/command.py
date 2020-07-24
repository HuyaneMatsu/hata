# -*- coding: utf-8 -*-
__all__ = ('Category', 'Command', 'CommandProcesser', 'checks', 'normalize_description', )

import re, reprlib

from ...backend.dereaddons_local import sortedlist, modulize, NEEDS_DUMMY_INIT
from ...backend.futures import Task
from ...backend.analyzer import CallableAnalyzer

from ...discord.others import USER_MENTION_RP
from ...discord.parsers import EventWaitforBase, compare_converted, check_name, check_argcount_and_convert
from ...discord.client_core import KOKORO

from .compiler import parse, COMMAND_CALL_SETTING_2ARGS, COMMAND_CALL_SETTING_3ARGS, COMMAND_CALL_SETTING_USE_PARSER

COMMAND_RP=re.compile(' *([^ \t\\n]*) *(.*)')

AUTO_DASH_MAIN_CHAR = '-'
AUTO_DASH_APPLICABLES = ('-', '_')

assert (len(AUTO_DASH_APPLICABLES)==0) or (AUTO_DASH_APPLICABLES != AUTO_DASH_APPLICABLES[0]), (
    f'`AUTO_DASH_MAIN_CHAR` (AUTO_DASH_MAIN_CHAR={AUTO_DASH_MAIN_CHAR!r} is not `AUTO_DASH_APPLICABLES[0]` '
    f'(AUTO_DASH_APPLICABLES={AUTO_DASH_APPLICABLES!r}!)')

class CommandWrapper(object):
    """
    Command wrapper what can be used for rich checks, which might return values to call their handler with.
    
    Attributes
    ----------
    wrapped : `async-callable`
        The wrapped function of the command.
    wrapper : `async-callable`
        Rich check, w
    """
    __slots__ = ('wrapped', 'wrapper', 'handler', )
    def __new__(cls, wrapped, wrapper, handler):
        """
        Creates a new ``CommandWrapper`` instance.
        
        Parameters
        ----------
        wrapped : `async-callable`
            The wrapped function.
        wrapper : `Any`
            A wrapper for the function.
        handler : None` or `async-callable`
            handler
        
        Returns
        -------
        self : ``CommandWrapper``
        """
        self = object.__new__(cls)
        self.wrapped = wrapped
        self.wrapper = wrapper
        self.handler = handler
        return self
    
    def __repr__(self):
        """Returns the command wrapper's representation."""
        return (f'{self.__class__.__name__}(wrapped={self.wrapped!r}, wrapper={self.wrapper!r}, '
            f'handler={self.handler!r})')

def generate_alters_for(name):
    """
    Generates alternative command names from the given one.
    
    Parameters
    ----------
    name : `str`
        A command's or an aliase's name.

    Returns
    -------
    alters : `list` of `str`
    """
    chars = []
    pattern = []
    for char in name:
        if char in AUTO_DASH_APPLICABLES:
            if chars:
                pattern.append(''.join(chars))
                chars.clear()
            
            pattern.append(None)
            continue
        
        chars.append(char)
        continue
    
    if chars:
        pattern.append(''.join(chars))
        chars.clear()
    
    alters = []
    if len(pattern) == 1:
        alters.append(pattern[0])
    
    else:
        generated = [[]]
        for part in pattern:
            if (part is not None):
                for generated_sub in generated:
                    generated_sub.append(part)
                continue
            
            count = len(generated)
            for _ in range(len(AUTO_DASH_APPLICABLES)-1):
                for index in range(count):
                    generated_sub = generated[index]
                    generated_sub = generated_sub.copy()
                    generated.append(generated_sub)
            
            index = 0
            for char in AUTO_DASH_APPLICABLES:
                for _ in range(count):
                    generated_sub = generated[index]
                    generated_sub.append(char)
                    
                    index+=1
        
        connected = [''.join(generated_sub) for generated_sub in generated]
        alters.extend(connected)
    
    return alters

COMMAND_CHECKS_FAILED = 0
COMMAND_CHECKS_SUCCEEDED = 1
COMMAND_CHECKS_HANDLED = 2
COMMAND_PARSER_FAILED = 3
COMMAND_SUCCEEDED = 4

class Command(object):
    """
    Represents a command object stored by a ``CommandProcesser`` in it's `.commands` and by a ``Category`` in it's
    ``.commands`` instance attribute.
    
    Attributes
    ----------
    aliases : `None` or `list` of `str`
        The aliases of the command stored at a sorted list. If it has no alises, this attribute will be set as `None`.
    category : `None` or ``Category``
        The commands's owner category.
    command : `async-callable`
        The async callable added as the command itself.
    description : `Any`
        Description added to the command. If no description is provided, then it will check the commands's `.__doc__`
        attribute for it. If the description is a string instance, then it will be normalized with the
        ``normalize_description`` function. If it ends up as an empty string, then `None` will be set as the
        description.
    name : `str`
        The command's name.
        
        > Always lower case.
    _alters : `set` of `str`
        Alternative name, whith what the command can be called.
    _call_setting : `int`
        An `int` flag, what defines, how the command should be called.
        
        Possible values:
        +-----------------------------------+-------+
        | Respective name                   | value |
        +===================================+=======+
        | COMMAND_CALL_SETTING_2ARGS        | 0     |
        +-----------------------------------+-------+
        | COMMAND_CALL_SETTING_3ARGS        | 1     |
        +-----------------------------------+-------+
        | COMMAND_CALL_SETTING_USE_PARSER   | 2     |
        +-----------------------------------+-------+
    _category_hint : `str` or `None`
        Hint for the command processer under which category should the give command go. If set as `None`, means that
        the command will go under the default category of the command processer.
    _checks : `None` or (`list` of ``_check_base`` instances)
        The internal slot used by the ``.checks`` property. Defaults to `None`.
    _parser : `None`
        The generated parser function for parsing the arguments to pass to the command. Defaults to `None`.
    _parser_failure_handler : `Any`
        The internal slot used by the ``.parser_failure_handler`` property. Defaults to `None`.
    _wrappers : `None`, `Any`, `list` of `async-callable`
        Additional wrappers, which run before the command is executed.
    """
    __slots__ = ( '_alters', '_call_setting', '_category_hint', '_checks', '_parser', '_parser_failure_handler',
        '_wrappers', 'aliases', 'category', 'command', 'description', 'name',)
    
    @classmethod
    def from_class(cls, klass, kwargs=None):
        """
        The method used, when creating a `Command` object from a class.
        
        > Extra `kwargs` are supported as well for the usecase.
        
        Parameters
        ----------
        klass : `type`
            The class, from what's attributes the command will be created.
            
            The expected attrbiutes of the given `klass` are the following:
            - name : `str` or `None`
                If was not defined, or was defined as `None`, the classe's name will be used.
            - command : `async-callable`
                If no `command` attribute was defined, then a attribute of the `name`'s value be checked as well.
            - description : `Any`
                If no description was provided, then the classe's `.__doc__` will be picked up.
            - aliases : `None` or (`iterable` of str`)
            - category : `None`, ``Category`` or `str`
            - checks : `None` or (`iterable` of ``_check_base``)
                If no checks were provided, then the classe's `.checks_` attribute will be checked as well.
            - parser_failure_handler : `None` or `async-callable`
        
        kwargs, `None` or `dict` of (`str`, `Any`) items, Optional
            Additional keyword arguments.
            
            The expected keyword arguments are the following:
            - description
            - category
            - checks
            - parser_failure_handler
        
        Returns
        -------
        command : ``Command``
        
        Raises
        ------
        TypeError
            - If `klass` was not given as `type` instance.
            - `kwargs` was not given as `None` and not all of it's items were used up.
            - `aliases` were not passed as `None` or as `iterable` of `str`.
            - `category` was not given as `None, `str`, or as ``Category`` instance.
            - If `checks` was not given as `None` or as `iterable` of ``_check_base`` instances.
        ValueError
            - If `.command` attribute is missing of the class.
        """
        klass_type = klass.__class__
        if not issubclass(klass_type, type):
            raise TypeError(f'Expected `type` instance, got {klass_type.__name__}.')
        
        name = getattr(klass,'name',None)
        if name is None:
            name = klass.__name__
        
        command = getattr(klass,'command',None)
        if command is None:
            while True:
                command = getattr(klass,name,None)
                if (command is not None):
                    break
                
                raise ValueError('`command` class attribute is missing.')
        
        
        description = getattr(klass,'description',None)
        if description is None:
            description = klass.__doc__
        
        aliases = getattr(klass,'aliases',None)
        
        category = getattr(klass,'category',None)
        
        checks_=getattr(klass,'checks',None)
        if checks_ is None:
            checks_=getattr(klass,'checks_',None)
        
        parser_failure_handler=getattr(klass,'parser_failure_handler',None)
        
        if (kwargs is not None) and kwargs:
            if (description is None):
                description = kwargs.pop('description', None)
            else:
                try:
                    del kwargs['description']
                except KeyError:
                    pass
            
            if (category is None):
                category = kwargs.pop('category', None)
            else:
                try:
                    del kwargs['category']
                except KeyError:
                    pass
            
            if (checks_ is None) or not checks_:
                checks_ = kwargs.pop('checks', None)
            else:
                try:
                    del kwargs['checks']
                except KeyError:
                    pass
            
            if (parser_failure_handler is None):
                parser_failure_handler = kwargs.pop('parser_failure_handler', None)
            else:
                try:
                    del kwargs['parser_failure_handler']
                except KeyError:
                    pass
            
            if kwargs:
                raise TypeError(f'`{cls.__name__}.from_class` did not use up some kwargs: `{kwargs!r}`.')
        
        return cls(command, name, description, aliases, category, checks_, parser_failure_handler)
    
    @classmethod
    def from_kwargs(cls, command, name, kwargs):
        """
        Called when a command is created before adding it to a ``CommandProcesser``.
        
        Parameters
        ----------
        command : `async-callable`
            The async callable added as the command itself.
        name : `str` or `None`
            The name to be used instead of the passed `command`'s.
        kwargs : `None` or `dict` of (`str`, `Any`) items.
            Additional keyword arguments.
            
            The expected keyword arguments are the following:
            - description : `Any`
            - aliases : `None` or (`iterable` of str`)
            - category : `None`, ``Category`` or `str`
            - checks : `None` or (`iterable` of ``_check_base``)
            - parser_failure_handler : `None` or `async-callable`
        
        Returns
        -------
        TypeError
            - `kwargs` was not given as `None` and not all of it's items were used up.
            - `aliases` were not passed as `None` or as `iterable` of `str`.
            - `category` was not given as `None, `str`, or as ``Category`` instance.
            - If `checks` was not given as `None` or as `iterable` of ``_check_base`` instances.
        """
        if (kwargs is None) or (not kwargs):
            description = None
            aliases = None
            category = None
            checks_ = None
            parser_failure_handler = None
        else:
            description = kwargs.pop('description',None)
            aliases = kwargs.pop('aliases',None)
            category = kwargs.pop('category',None)
            checks_ = kwargs.pop('checks',None)
            parser_failure_handler = kwargs.pop('parser_failure_handler',None)
            
            if kwargs:
                raise TypeError(f'type `{cls.__name__}` not uses: `{kwargs!r}`.')
        
        return cls(command, name, description, aliases, category, checks_, parser_failure_handler)
    
    def __new__(cls, command, name, description, aliases, category, checks_, parser_failure_handler):
        """
        Creates a new ``Command`` object.
        
        Parameters
        ----------
        command : `async-callable`
            The async callable added as the command itself.
        name : `str` or `None`
            The name to be used instead of the passed `command`'s.
        description : `Any`
            Description added to the command. If no description is provided, then it will check the commands's
            `.__doc__` attribute for it. If the description is a string instance, then it will be normalized with the
            ``normalize_description`` function. If it ends up as an empty string, then `None` will be set as the
            description.
        aliases : `None` or (`iterable` of `str`)
            The aliases of the command.
        category : `None`, ``Category`` or `str` instance
            The category of the command. Can be given as the category itself, or as a category's name. If given as
            `None`, then the command will go under the command processer's default category.
        checks_ : `None` or (`iterable` of ``_check_base`` instances)
            Checks to deside in which circumstances the command should be called.
        
        parser_failure_handler : `None` or `async-callable`
            Called when the command uses a parser to parse it's arguments, but it cannot parse out all the required
            ones.
            
            If given as an `async-callable`, then it should accept 5 arguments:
            
            +-----------------------+-------------------+
            | Respective name       | Type              |
            +=======================+===================+
            | client                | ``Client``        |
            +-----------------------+-------------------+
            | message               | ``Message``       |
            +-----------------------+-------------------+
            | command               | ``Command``       |
            +-----------------------+-------------------+
            | content               | `str`             |
            +-----------------------+-------------------+
            | args                  | `list` of `Any`   |
            +-----------------------+-------------------+
        
        Returns
        -------
        command : ``Command``
        
        Raises
        ------
        TypeError
            - `aliases` were not passed as `None` or as `iterable` of `str`.
            - `category` was not given as `None, `str`, or as ``Category`` instance.
            - If `checks_` was not given as `None` or as `iterable` of ``_check_base`` instances.
        """
        
        wrappers = None
        while isinstance(command, CommandWrapper):
            if wrappers is None:
                wrappers = command
            elif type(wrappers) is list:
                wrappers.append(command)
            else:
                wrappers = [wrappers, command]
            
            command = command.wrapped
        
        name = check_name(command,name)
        
        # Check aliases
        aliases_checked = []
        
        if (aliases is not None):
            aliases_type = aliases.__class__
            if issubclass(aliases_type, str) or (not hasattr(aliases_type, '__iter__')):
                raise TypeError(f'`aliases` should have be passed as `None` or as an `iterable` of `str`, got '
                    f'{aliases_type.__class__}.')
            
            index = 1
            for alias in aliases:
                alias_type = alias.__class__
                if alias_type is str:
                    pass
                elif issubclass(alias_type, str):
                    alias = str(alias)
                else:
                    raise TypeError(f'Element {index} of `aliases` should have been `str` instance, meanwhile got '
                        f'{alias_type.__name__}.')
                
                aliases_checked.append(alias)
        
        alters = set()
        alters_sub = generate_alters_for(name)
        name = alters_sub[0]
        alters.update(alters_sub)
        
        aliases = set()
        for alias in aliases_checked:
            alters_sub = generate_alters_for(alias)
            aliases.add(alters_sub[0])
            alters.update(alters_sub)
        
        try:
            aliases.remove(name)
        except KeyError:
            pass
        
        if aliases:
            aliases = sorted(aliases)
        else:
            aliases = None
        
        if description is None:
            description=getattr(command,'__doc__',None)
        
        if (description is not None) and isinstance(description,str):
            description=normalize_description(description)
        
        if category is None:
            category_hint = None
        else:
            category_type = category.__class__
            if category_type is Category:
                category_hint = category.name
                category = category
            elif category_type is str:
                category_hint = category
                category = None
            elif issubclass(category_type, str):
                category = str(category)
                category_hint = category
                category = None
            else:
                raise TypeError(f'`category` should be `None`, type `str` or `{Category.__name__}`, got '
                    f'{category_type.__name__}.')
        
        checks_processed = validate_checks(checks_)
        
        if (parser_failure_handler is not None):
            parser_failure_handler = check_argcount_and_convert(parser_failure_handler, 5,
                '`parser_failure_handler` expected 5 arguments (client, message, command, content, args).')
        
        command, call_setting, parser = parse(command)
        
        self=object.__new__(cls)
        self.command        = command
        self.name           = name
        self.aliases        = aliases
        self.description    = description
        self.category       = category
        self._alters        = alters
        self._call_setting  = call_setting
        self._category_hint = category_hint
        self._checks        = checks_processed
        self._parser        = parser
        self._wrappers      = wrappers
        self._parser_failure_handler = parser_failure_handler
        
        return self
    
    def __repr__(self):
        """Returns the command's representation."""
        result = [
            '<',
            self.__class__.__name__,
            ' name=',
            repr(self.name),
            ', command=',
            repr(self.command),
                ]
        
        description=self.description
        if (description is not None):
            result.append(', description=')
            result.append(reprlib.repr(self.description))
        
        aliases=self.aliases
        if (aliases is not None):
            result.append(', aliases=')
            result.append(repr(aliases))
        
        checks=self._checks
        if (checks is not None):
            result.append(', checks=')
            result.append(repr(checks))
        
        result.append(', category=')
        result.append(repr(self.category))
        
        call_setting=self._call_setting
        if call_setting != COMMAND_CALL_SETTING_2ARGS:
            if call_setting == COMMAND_CALL_SETTING_3ARGS:
                result.append(', call with content')
            else:
                result.append(', use parser')
            
            parser_failure_handler=self.parser_failure_handler
            if (parser_failure_handler is not None):
                result.append(', parser_failure_handler=')
                result.append(repr(parser_failure_handler))
            
        result.append('>')
        
        return ''.join(result)
    
    def __str__(self):
        """Returns the command's name."""
        return self.name
    
    def _get_checks(self):
        checks = self._checks
        if (checks is not None):
            checks = checks.copy()
        
        return checks
    
    def _set_checks(self, checks_):
        self._checks = validate_checks(checks_)
    
    def _del_checks(self):
        self._checks = None
    
    checks = property(_get_checks, _set_checks, _del_checks)
    del _get_checks, _set_checks, _del_checks
    
    if (__new__.__doc__ is not None):
        checks.__doc__ = ("""
        Get-set-del property for accessing the checks of the ``Command``.
        
        When using it is get property returns the checks of the command, what can be `None` or `list` of
        ``_check_base`` instances.
        
        When setting it, accepts `None` or an `iterable` of ``_check_base`` instances. Raises `TypeError` if invalid
        type or element type is given.
        
        By deleting it removes the command's checks.
        """)
    
    def _get_parser_failure_handler(self):
        return self._parser_failure_handler
    
    def _set_parser_failure_handler(self, parser_failure_handler):
        if parser_failure_handler is None:
            return
        
        parser_failure_handler = check_argcount_and_convert(parser_failure_handler, 5,
            '`parser_failure_handler` expected 5 arguments (client, message, command, content, args).')
        self._parser_failure_handler=parser_failure_handler
    
    def _del_parser_failure_handler(self):
        self._parser_failure_handler=None
    
    parser_failure_handler = property(_get_parser_failure_handler, _set_parser_failure_handler, _del_parser_failure_handler)
    del _get_parser_failure_handler, _set_parser_failure_handler, _del_parser_failure_handler
    
    if (__new__.__doc__ is not None):
        parser_failure_handler.__doc__ = ("""
        Get-set-del property for accessing the ``Command``'s parser failure handler.
        
        Can be set as `None` or as an `async-callable`, what accepts the following 5 arguments:
        +-----------------------+-------------------+
        | Respective name       | Type              |
        +=======================+===================+
        | client                | ``Client``        |
        +-----------------------+-------------------+
        | message               | ``Message``       |
        +-----------------------+-------------------+
        | command               | ``Command``       |
        +-----------------------+-------------------+
        | content               | `str`             |
        +-----------------------+-------------------+
        | args                  | `list` of `Any`   |
        +-----------------------+-------------------+
        
        If a bad type was given or if the given value accepts bad amount of non reserved positional arguments, then
        `TypeError` is raised.
        
        When deleting it removes the commands's parser failure handler.
        """)
    
    async def __call__(self, client, message, content):
        """
        Calls the command.
        
        The command has the following run process:
        
        Calls the command's category's checks, then the command's checks. If a check passes, the next check is called,
        till there are no checks left or till one fails. If a check fails, then it `.handler` will be ensured if
        applicable.
        
        At the next step the call options of the command are checked, and if needed the command's parser is ensured.
        If the parser could not parse out all the required arguments, then the command's `parser_failure_handler` is
        called if applicable.
        
        Note that not the command handles the exceptions dropped by the command, but the command processer does.
        
        Parameters
        ----------
        client : ``Client``
            The client with who the command will be called with.
        message : ``Message``
            The message with what the command will be called with.
        content : `str`
            The message's content after the prefix and the command's name, but before the first linebreak.
            Can be empty string.
        
        Returns
        -------
        result : `int`
            Returns an identificator number depending how the command execution went.
            
            Possible values:
            +---------------------------+-------+
            | Respective name           |Value  |
            +===========================+=======+
            | COMMAND_CHECKS_FAILED     | 0     |
            +---------------------------+-------+
            | COMMAND_CHECKS_HANDLED    | 2     |
            +---------------------------+-------+
            | COMMAND_PARSER_FAILED     | 3     |
            +---------------------------+-------+
            | COMMAND_SUCCEEDED         | 4     |
            +---------------------------+-------+
        """
        category = self.category
        if (category is not None):
            checks = category._checks
            if (checks is not None):
                for check in checks:
                    if await check(client, message):
                        continue
                    
                    handler = check.handler
                    if (handler is None):
                        return COMMAND_CHECKS_FAILED
                    
                    await handler(client, message, self, check)
                    return COMMAND_CHECKS_HANDLED
        
        checks = self._checks
        if (checks is not None):
            for check in checks:
                if await check(client, message):
                    continue
                
                handler = check.handler
                if (handler is None):
                    return COMMAND_CHECKS_FAILED
                
                await handler(client, message, self, check)
                return COMMAND_CHECKS_HANDLED
        
        command_wrapper = self._wrappers
        if (command_wrapper is not None):
            if type(command_wrapper) is list:
                for command_wrapper in command_wrapper:
                    gen = command_wrapper.wrapper(client, message)
                    result = await gen.asend(None)
                    if result:
                        gen.aclose()
                    else:
                        handler = command_wrapper.handler
                        if (handler is None):
                            gen.aclose()
                        else:
                            args = []
                            async for arg in gen:
                                args.append(arg)
                            await handler(client, message, self, *args)
                        return
            else:
                gen = command_wrapper.wrapper(client, message)
                result = await gen.asend(None)
                if result:
                    gen.aclose()
                else:
                    handler = command_wrapper.handler
                    if (handler is None):
                        gen.aclose()
                    else:
                        args = []
                        async for arg in gen:
                            args.append(arg)
                        await handler(client, message, self, *args)
                    return COMMAND_PARSER_FAILED
        
        call_setting = self._call_setting
        if call_setting == COMMAND_CALL_SETTING_USE_PARSER:
            passed, args = await self._parser(client, message, content)
            if not passed:
                parser_failure_handler = self._parser_failure_handler
                if (parser_failure_handler is not None):
                    await parser_failure_handler(client, message, self, content, args)
                
                return COMMAND_PARSER_FAILED
            
            coro = self.command(client, message, *args)
        
        elif call_setting == COMMAND_CALL_SETTING_2ARGS:
            coro = self.command(client, message)
        
        else:
            # last case: COMMAND_CALL_SETTING_3ARGS
            coro = self.command(client, message, content)
        
        await coro
        return COMMAND_SUCCEEDED
    
    async def call_checks(self, client, message, content):
        """
        Runs the checks of the commands's ``.category`` and of the command itself too.
        
        Acts familiarly to ``.__call__``, but it returns `False` at the end of the checks, instead of continuing.
        
        Parameters
        ----------
        client : ``Client``
            The client with what the checks will be called.
        message : ``Message``
            The message with what the checks will be called.
        content : `str`
            The message's content after the prefix and the command's name, but before the first linebreak.
            Can be empty string.
        
        Returns
        -------
        result : `int`
            Returns an identificator number depending how the command execution went.
            
            Possible values:
            +---------------------------+-------+
            | Respective name           |Value  |
            +===========================+=======+
            | COMMAND_CHECKS_FAILED     | 0     |
            +---------------------------+-------+
            | COMMAND_CHECKS_SUCCEEDED  | 1     |
            +---------------------------+-------+
            | COMMAND_CHECKS_HANDLED    | 2     |
            +---------------------------+-------+
        """
        category = self.category
        if (category is not None):
            checks = category._checks
            if (checks is not None):
                for check in checks:
                    if await check(client, message):
                        continue
                    
                    handler = check.handler
                    if (handler is None):
                        return COMMAND_CHECKS_FAILED
                    
                    await handler(client, message, self, check)
                    return COMMAND_CHECKS_HANDLED
                    
                
        checks = self._checks
        if (checks is not None):
            for check in checks:
                if await check(client, message):
                    continue
                
                handler = check.handler
                if (handler is None):
                    return COMMAND_CHECKS_FAILED
                
                await handler(client, message, self, check)
                return COMMAND_CHECKS_HANDLED
        
        return COMMAND_CHECKS_SUCCEEDED
    
    async def run_all_checks(self, client, message):
        """
        Runs all the checks of the command's category and of the command and returns `True` if every of passes.
        
        Parameters
        ----------
        client : ``Client``
            The client with what the checks will be called.
        message : ``Message``
            The message with what the checks will be called.
        
        Returns
        -------
        result : `int`
            Returns an identificator number depending how the command execution went.
            
            Possible values:
            +---------------------------+-------+
            | Respective name           |Value  |
            +===========================+=======+
            | COMMAND_CHECKS_FAILED     | 0     |
            +---------------------------+-------+
            | COMMAND_CHECKS_SUCCEEDED  | 1     |
            +---------------------------+-------+
        """
        category = self.category
        if (category is not None):
            checks = category._checks
            if (checks is not None):
                for check in checks:
                    if await check(client, message):
                        continue
                    
                    return COMMAND_CHECKS_FAILED
        
        checks = self._checks
        if (checks is not None):
            for check in checks:
                if await check(client, message):
                    continue
                
                return COMMAND_CHECKS_FAILED
        
        return COMMAND_CHECKS_SUCCEEDED
    
    async def run_checks(self, client, message):
        """
        Runs all the checks of the command and returns whether every of them passed.
        
        Parameters
        ----------
        client : ``Client``
            The client with what the checks will be called.
        message : ``Message``
            The message with what the checks will be called.
        
        Returns
        -------
        result : `int`
            Returns an identificator number depending how the command execution went.
            
            Possible values:
            +---------------------------+-------+
            | Respective name           |Value  |
            +===========================+=======+
            | COMMAND_CHECKS_FAILED     | 0     |
            +---------------------------+-------+
            | COMMAND_CHECKS_SUCCEEDED  | 1     |
            +---------------------------+-------+
        """
        checks = self._checks
        if (checks is not None):
            for check in checks:
                if await check(client, message):
                    continue
                
                return COMMAND_CHECKS_FAILED
        
        return COMMAND_CHECKS_SUCCEEDED
    
    async def call_command(self, client, message, content):
        """
        Runs the command's function.
        
        Acts familiarly as ``.__call__``, but without it's checks.
        
        Parameters
        ----------
        client : ``Client``
            The client with what the command will be called.
        message : ``Message``
            The message with what the command will be called.
        content : `str`
            The message's content after the prefix and the command's name, but before the first linebreak.
            Can be empty string.
        
        Returns
        -------
        result : `bool`
            Returns `True` indicating that the command (or a handler run).
        """
        call_setting = self._call_setting
        if call_setting == COMMAND_CALL_SETTING_USE_PARSER:
            passed, args = await self._parser(client, message, content)
            if not passed:
                parser_failure_handler = self._parser_failure_handler
                if (parser_failure_handler is not None):
                    await parser_failure_handler(client, message, self, content, args)
                
                return COMMAND_PARSER_FAILED
            
            coro = self.command(client, message, *args)
            
        elif call_setting == COMMAND_CALL_SETTING_2ARGS:
            coro = self.command(client, message)
        
        else:
            # last case: COMMAND_CALL_SETTING_3ARGS
            coro = self.command(client, message, content)
        
        await coro
        return COMMAND_SUCCEEDED
    
    def __getattr__(self, name):
        """Tries to return the attribute of the command's function."""
        wrappers = self._wrappers
        if wrappers is None:
            obj = self.command
        else:
            if type(wrappers) is list:
                obj = wrappers[0]
            else:
                obj = wrappers
        
        return getattr(obj, name)
    
    def __gt__(self, other):
        """Returns whether this command's name is greater than the other's"""
        return self.name>other.name
    
    def __lt__(self, other):
        """Returns whether this command's name is less than the other's"""
        return self.name<other.name

def normalize_description(text):
    """
    Normalizes a passed string with right stripping every line, with removing every empty line from it's start and
    from it's end, and with dedenting.
    
    Parameters
    ----------
    text : `str`
        Docstring to normalize.
    
    Returns
    -------
    result : `None` or `str`
        The normalized description, or `None` if ended up with an empty string.
    """
    lines=text.splitlines()
    
    for index in range(len(lines)):
        lines[index]=lines[index].rstrip()
    
    while True:
        if not lines:
            return None
        
        line=lines[0]
        if line:
            break
        
        del lines[0]
        continue
    
    while True:
        if not lines:
            return None
        
        line=lines[-1]
        if line:
            break
        
        del lines[-1]
        continue
    
    limit=len(lines)
    if limit==1:
        return lines[0].lstrip()
    
    ignore_index=0
    
    while True:
        next_char=lines[0][ignore_index]
        if next_char not in ('\t', ' '):
            break
        
        index=1
        while index<limit:
            line=lines[index]
            index=index+1
            if not line:
                continue
            
            char=line[ignore_index]
            if char!=next_char:
                break
            
            continue
        
        if char!=next_char:
            break
        
        ignore_index=ignore_index+1
        continue
    
    if ignore_index!=0:
        for index in range(len(lines)):
            line=lines[index]
            if not line:
                continue
            
            lines[index]=line[ignore_index:]
            continue
    
    return '\n'.join(lines)

@modulize
class checks:
    from ...discord.bases import instance_or_id_to_instance, instance_or_id_to_snowflake
    from ...discord.guild import Guild
    from ...discord.permission import Permission
    from ...discord.role import Role
    from ...discord.channel import ChannelBase
    from ...discord.parsers import check_argcount_and_convert
    
    def validate_checks(checks_):
        """
        Validates the given checks.
        
        checks_ : `None` or (`iterable` of ``_check_base`` instances), Optional
            Checks to define in which circumstances a command should be called.
            
        Returns
        -------
        checks_processed : `None` or `list` of ``_check_base``
            Will never return an empty list.
        
        Raises
        ------
        TypeError
            If `checks_` was not given as `None` or as `iterable` of ``_check_base`` instances.
        """
        if checks_ is None:
            checks_processed = None
        else:
            checks_type = checks_.__class__
            if hasattr(checks_type, '__iter__'):
                checks_processed = []
                
                index = 1
                for check in checks_:
                    check_type = check.__class__
                    if issubclass(check_type, _check_base):
                        checks_processed.append(check)
                        index +=1
                        continue
                    
                    raise TypeError(f'`checks` element {index} was not given as `{_check_base.__name__}`, got '
                        f'`{check_type.__name__}`.')
                
                if not checks_processed:
                    checks_processed=None
            else:
                raise TypeError(f'`checks_` should have been given as `None` or as `iterable` of '
                    f'`{_check_base.__name__}` instances, got {checks_type.__name__}.')
            
            if not checks_processed:
                checks_processed = None
        
        return checks_processed
    
    def _convert_handler(handler):
        """
        Validates the given handler.
        
        Parameters
        ----------
        handler : `None` or `async-callable` or instanceable to `async-callable`
            The handler to convert.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the following
            arguments:
            +-------------------+---------------------------+
            | Respective name   | Type                      |
            +===================+===========================+
            | client            | ``Client``                |
            +-------------------+---------------------------+
            | message           | ``Message``               |
            +-------------------+---------------------------+
            | command           | ``Command``               |
            +-------------------+---------------------------+
            | check             | ``_check_base`` instance  |
            +-------------------+---------------------------+
        
        Returns
        -------
        handler : `None` or `async-callable`
        
        Raises
        ------
        TypeError
            If `handler` was given as an invalid type, or it accepts a bad amount of arguments.
        """
        if (handler is not None):
            handler = check_argcount_and_convert(handler, 4, '`handler` expects to pass 4 arguments (client, '
                'message, command, check).')
        return handler
    
    def _convert_permissions(permissions):
        """
        Validates the given `permissions`.
        
        Parameters
        ----------
        permissions : ``Permission`` or `int` instance
            Permission to validate.
        
        Returns
        -------
        permissions : ``Permission``
        
        Raises
        ------
        TypeError
            `permissions` was not given as `int` instance.
        """
        permission_type = permissions.__class__
        if permission_type is Permission:
            pass
        elif issubclass(permission_type, int):
            permissions = Permission(permissions)
        else:
            raise TypeError(f'`permissions` should have been passed as a `{Permission.__name__}` object or as an '
                f'`int` instance, got {permission_type.__name__}.')
        
        return permissions
    
    class _check_base(object):
        """
        Base class for checks.
        
        Attributes
        ----------
        handler : `None` or `async-callable`
            An async callable what will be called when the check fails.
        """
        __slots__ = ('handler',)
        def __new__(cls, handler=None):
            """
            Creates a check with the given paramteres.
            
            Paramaters
            ----------
            handler : `None` or `async-callable` or instanceable to `async-callable`
                Will be called when the check fails.
                
                If the handler is `async-callable` or if it would be instanced to it, then it should accept the
                following arguments:
                +-------------------+---------------------------+
                | Respective name   | Type                      |
                +===================+===========================+
                | client            | ``Client``                |
                +-------------------+---------------------------+
                | message           | ``Message``               |
                +-------------------+---------------------------+
                | command           | ``Command``               |
                +-------------------+---------------------------+
                | check             | ``_check_base`` instance  |
                +-------------------+---------------------------+
            
            Raises
            ------
            TypeError
                If `handler` was given as an invalid type, or it accepts a bad amount of arguments.
            """
            handler = _convert_handler(handler)
            self = object.__new__(cls)
            self.handler = handler
            return self
        
        async def __call__(self, client, message):
            """
            Calls the check to validate whether it passes with the given conditions.
            
            Subclasses should overwrite this method.
            
            Parameters
            ----------
            client : ``Client``
                The client who's received the message.
            message : ``Message``
                The received message.
            
            Returns
            -------
            passed : `bool`
                Whether the check passed.
            """
            return True
        
        def __repr__(self):
            """Returns the check's representation."""
            result = [
                self.__class__.__name__,
                '(',
                    ]
            
            slots=self.__slots__
            limit=len(slots)
            if limit:
                index=0
                while True:
                    name=slots[index]
                    index=index+1
                    # case of `_is_async`
                    if name.startswith('_'):
                        continue
                    
                    # case of `channel_id`, `guild_id`
                    if name.endswith('id'):
                        name = name[:-3]
                    # case of `channel_ids`, `guild_ids`
                    elif name.endswith('ids'):
                        name = name[:-4]
                    
                    result.append(name)
                    result.append('=')
                    attr=getattr(self,name)
                    result.append(repr(attr))
                    
                    if index==limit:
                        break
                    
                    result.append(', ')
                    continue
            
            handler = self.handler
            if (handler is not None):
                if limit:
                    result.append(', ')
                result.append('handler=')
                result.append(repr(handler))
            
            result.append(')')
            
            return ''.join(result)
        
        if NEEDS_DUMMY_INIT:
            def __init__(self, *args, **kwargs):
                pass
    
    class has_role(_check_base):
        """
        Checks whether a message's author has the given role.
        
        Attributes
        ----------
        handler : `None` or `async-callable`
            An async callable what will be called when the check fails.
        role : ``Role``
            The role, what the user should have.
        """
        __slots__ = ('role', )
        def __new__(cls, role, handler=None):
            """
            Creates a check, what will validate whether the a received message of a client passes the given condition.
            
            Parameters
            ----------
            role : `str`, `int` or ``Role``
                The role what the message's author should have.
            handler : `None` or `async-callable` or instanceable to `async-callable`
                Will be called when the check fails.
                
                If the handler is `async-callable` or if it would be instanced to it, then it should accept the
                following arguments:
                +-------------------+---------------------------+
                | Respective name   | Type                      |
                +===================+===========================+
                | client            | ``Client``                |
                +-------------------+---------------------------+
                | message           | ``Message``               |
                +-------------------+---------------------------+
                | command           | ``Command``               |
                +-------------------+---------------------------+
                | check             | ``_check_base`` instance  |
                +-------------------+---------------------------+
            
            Raises
            ------
            TypeError
                - If `role` was not given neither as ``Role``, `str` or `int` instance.
                - If `handler` was given as an invalid type, or it accepts a bad amount of arguments.
            ValueError
                If `role` was given as `str` or as `int` instance, but not as a valid snowflake, so ``Role``
                    instance cannot be precreated with it.
            """
            role = instance_or_id_to_instance(role, Role)
            handler = _convert_handler(handler)
            
            self = object.__new__(cls)
            self.role = role
            self.handler = handler
            return self
        
        async def __call__(self, client, message):
            """
            Calls the check to validate whether it passes with the given conditions.
            
            Parameters
            ----------
            client : ``Client``
                The client who's received the message.
            message : ``Message``
                The received message.
            
            Returns
            -------
            passed : `bool`
                Whether the check passed.
            """
            if message.author.has_role(self.role):
                return True
            
            return False
    
    class owner_or_has_role(has_role):
        """
        Checks whether a message's author has the given role, or if it the client's owner.
        
        Attributes
        ----------
        handler : `None` or `async-callable`
            An async callable what will be called when the check fails.
        role : ``Role``
            The role, what the user should have.
        """
        async def __call__(self, client, message):
            """
            Calls the check to validate whether it passes with the given conditions.
            
            Parameters
            ----------
            client : ``Client``
                The client who's received the message.
            message : ``Message``
                The received message.
            
            Returns
            -------
            passed : `bool`
                Whether the check passed.
            """
            user = message.author
            if user.has_role(self.role):
                return True
            
            if client.is_owner(user):
                return True
            
            return False
    
    class has_any_role(_check_base):
        """
        Checks whether a message's author has any of the given roles.
        
        Attributes
        ----------
        handler : `None` or `async-callable`
            An async callable what will be called when the check fails.
        roles : `set` of ``Role``
            The roles from what the user should have at least 1.
        """
        __slots__ = ('roles', )
        def __new__(cls, roles, handler=None):
            """
            Creates a check, what will validate whether the a received message of a client passes the given condition.
            
            Parameters
            ----------
            roles : `iterable` of (`str`, `int` or ``Role``)
                Role from what the message's author should have at least 1.
            handler : `None` or `async-callable` or instanceable to `async-callable`
                The handler to convert.
                
                If the handler is `async-callable` or if it would be instanced to it, then it should accept the
                following arguments:
                +-------------------+---------------------------+
                | Respective name   | Type                      |
                +===================+===========================+
                | client            | ``Client``                |
                +-------------------+---------------------------+
                | message           | ``Message``               |
                +-------------------+---------------------------+
                | command           | ``Command``               |
                +-------------------+---------------------------+
                | check             | ``_check_base`` instance  |
                +-------------------+---------------------------+
            
            Raises
            ------
            TypeError
                - If `roles` was not given as an `iterable`.
                - If an element of `roles` was not given neither as ``Role``, `str` or `int` instance.
                - If `handler` was given as an invalid type, or it accepts a bad amount of arguments.
            ValueError
                If an element of `roles` was given as `str` or as `int` instance, but not as a valid snowflake, so
                    ``Role`` instance cannot be precreated with it.
            """
            roles_type = roles.__class__
            if not hasattr(roles_type,'__iter__'):
                raise TypeError(f'`roles` can be given as `iterable` of (`str`, `int` or `{Role.__name__}`, got '
                    f'{roles_type.__name__}.')
            
            roles_processed = set()
            for role in roles:
                role = instance_or_id_to_instance(role, Role)
                roles_processed.add(role)
            
            self = object.__new__(cls)
            self.roles = roles_processed
            self.handler = _convert_handler(handler)
            return self
        
        async def __call__(self, client, message):
            """
            Calls the check to validate whether it passes with the given conditions.
            
            Parameters
            ----------
            client : ``Client``
                The client who's received the message.
            message : ``Message``
                The received message.
            
            Returns
            -------
            passed : `bool`
                Whether the check passed.
            """
            user=message.author
            if user.has_role(self.roles):
                return True
            
            return False
    
    class owner_or_has_any_role(has_any_role):
        """
        Checks whether a message's author has any of the given roles or if it is the client's owner.
        
        Attributes
        ----------
        handler : `None` or `async-callable`
            An async callable what will be called when the check fails.
        roles : `set` of ``Role``
            The roles from what the user should have at least 1.
        """
        async def __call__(self, client, message):
            """
            Calls the check to validate whether it passes with the given conditions.
            
            Parameters
            ----------
            client : ``Client``
                The client who's received the message.
            message : ``Message``
                The received message.
            
            Returns
            -------
            passed : `bool`
                Whether the check passed.
            """
            user=message.author
            for role in self.roles:
                if user.has_role(role):
                    return True
            
            if client.is_owner(user):
                return True
            
            return False
    
    class guild_only(_check_base):
        """
        Checks whether a message was sent to a guild channel.
        
        Attributes
        ----------
        handler : `None` or `async-callable`
            An async callable what will be called when the check fails.
        """
        __slots__ = ()
        
        async def __call__(self, client, message):
            """
            Calls the check to validate whether it passes with the given conditions.
            
            Parameters
            ----------
            client : ``Client``
                The client who's received the message.
            message : ``Message``
                The received message.
            
            Returns
            -------
            passed : `bool`
                Whether the check passed.
            """
            if (message.guild is not None):
                return True
            
            return False
    
    class private_only(_check_base):
        """
        Checks whether a message was sent to a private channel.
        
        Attributes
        ----------
        handler : `None` or `async-callable`
            An async callable what will be called when the check fails.
        """
        __slots__ = ()
        async def __call__(self, client, message):
            """
            Calls the check to validate whether it passes with the given conditions.
            
            Parameters
            ----------
            client : ``Client``
                The client who's received the message.
            message : ``Message``
                The received message.
            
            Returns
            -------
            passed : `bool`
                Whether the check passed.
            """
            if (message.guild is None):
                return True
            
            return False
    
    class owner_only(_check_base):
        """
        Checks whether a message was sent by the client's owner.
        
        Attributes
        ----------
        handler : `None` or `async-callable`
            An async callable what will be called when the check fails.
        """
        __slots__ = ()
        async def __call__(self, client, message):
            """
            Calls the check to validate whether it passes with the given conditions.
            
            Parameters
            ----------
            client : ``Client``
                The client who's received the message.
            message : ``Message``
                The received message.
            
            Returns
            -------
            passed : `bool`
                Whether the check passed.
            """
            if client.is_owner(message.author):
                return True
            
            return False
    
    class guild_owner(_check_base):
        """
        Checks whether a message was sent by the message's guild's owner.
        
        Attributes
        ----------
        handler : `None` or `async-callable`
            An async callable what will be called when the check fails.
        """
        __slots__ = ()
        async def __call__(self, client, message):
            """
            Calls the check to validate whether it passes with the given conditions.
            
            Parameters
            ----------
            client : ``Client``
                The client who's received the message.
            message : ``Message``
                The received message.
            
            Returns
            -------
            passed : `bool`
                Whether the check passed.
            """
            guild = message.channel.guild
            if guild is None:
                return False
            
            if guild.owner==message.author:
                return True
            
            return False
    
    class owner_or_guild_owner(guild_owner):
        """
        Checks whether a message was sent by the message's guild's owner or by the client's owner.
        
        Attributes
        ----------
        handler : `None` or `async-callable`
            An async callable what will be called when the check fails.
        """
        __slots__ = ()
        async def __call__(self, client, message):
            """
            Calls the check to validate whether it passes with the given conditions.
            
            Parameters
            ----------
            client : ``Client``
                The client who's received the message.
            message : ``Message``
                The received message.
            
            Returns
            -------
            passed : `bool`
                Whether the check passed.
            """
            guild = message.channel.guild
            if guild is None:
                return False
            
            user = message.author
            if guild.owner==user:
                return True
            
            if client.is_owner(user):
                return True
            
            return False
    
    class has_permissions(_check_base):
        """
        Checks whether a message's author has the given permissions at the message's channel.
        
        Attributes
        ----------
        handler : `None` or `async-callable`
            An async callable what will be called when the check fails.
        permissions : ``Permission``
            The permission what the message's author should have at message's channel.
        """
        __slots__ = ('permissions', )
        def __new__(cls, permissions, handler=None):
            """
            Creates a check, what will validate whether the a received message of a client passes the given condition.
            
            Parameters
            ----------
            permissions : ``Permission`` or `in` instance
                The permisison, what the message's author should have at the message's channel.
            handler : `None` or `async-callable` or instanceable to `async-callable`
                The handler to convert.
                
                If the handler is `async-callable` or if it would be instanced to it, then it should accept the
                following arguments:
                +-------------------+---------------------------+
                | Respective name   | Type                      |
                +===================+===========================+
                | client            | ``Client``                |
                +-------------------+---------------------------+
                | message           | ``Message``               |
                +-------------------+---------------------------+
                | command           | ``Command``               |
                +-------------------+---------------------------+
                | check             | ``_check_base`` instance  |
                +-------------------+---------------------------+
            
            Raises
            ------
            TypeError
                - `permissions` was not given as `int` instance.
                - If `handler` was given as an invalid type, or it accepts a bad amount of arguments.
            """
            permissions = _convert_permissions(permissions)
            handler = _convert_handler(handler)
            
            self = object.__new__(cls)
            self.permissions = permissions
            self.handler = handler
            return self
        
        async def __call__(self, client, message):
            """
            Calls the check to validate whether it passes with the given conditions.
            
            Parameters
            ----------
            client : ``Client``
                The client who's received the message.
            message : ``Message``
                The received message.
            
            Returns
            -------
            passed : `bool`
                Whether the check passed.
            """
            if message.channel.permissions_for(message.author)>=self.permissions:
                return True
            
            return False
    
    class owner_or_has_permissions(has_permissions):
        """
        Checks whether a message's author has the given permissions at the message's channel, or if it is the client's
        owner.
        
        Attributes
        ----------
        handler : `None` or `async-callable`
            An async callable what will be called when the check fails.
        permissions : ``Permission``
            The permission what the message's author should have at message's channel.
        """
        async def __call__(self, client, message):
            """
            Calls the check to validate whether it passes with the given conditions.
            
            Parameters
            ----------
            client : ``Client``
                The client who's received the message.
            message : ``Message``
                The received message.
            
            Returns
            -------
            passed : `bool`
                Whether the check passed.
            """
            user = message.author
            if message.channel.permissions_for(user)>=self.permissions:
                return True
            
            if client.is_owner(user):
                return True
            
            return False
    
    class has_guild_permissions(_check_base):
        """
        Checks whether a message's author has the given permissions at the message's guild.
        
        Attributes
        ----------
        handler : `None` or `async-callable`
            An async callable what will be called when the check fails.
        permissions : ``Permission``
            The permission what the message's author should have at message's guild.
        """
        __slots__ = ('permissions', )
        def __new__(cls, permissions, handler=None):
            """
            Creates a check, what will validate whether the a received message of a client passes the given condition.
            
            Parameters
            ----------
            permissions : ``Permission`` or `in` instance
                The permisison, what the message's author should have at the message's guild.
            handler : `None` or `async-callable` or instanceable to `async-callable`
                The handler to convert.
                
                If the handler is `async-callable` or if it would be instanced to it, then it should accept the
                following arguments:
                +-------------------+---------------------------+
                | Respective name   | Type                      |
                +===================+===========================+
                | client            | ``Client``                |
                +-------------------+---------------------------+
                | message           | ``Message``               |
                +-------------------+---------------------------+
                | command           | ``Command``               |
                +-------------------+---------------------------+
                | check             | ``_check_base`` instance  |
                +-------------------+---------------------------+
            
            Raises
            ------
            TypeError
                - `permissions` was not given as `int` instance.
                - If `handler` was given as an invalid type, or it accepts a bad amount of arguments.
            """
            permissions = _convert_permissions(permissions)
            handler = _convert_handler(handler)
            
            self = object.__new__(cls)
            self.permissions = permissions
            self.handler = handler
            return self
        
        async def __call__(self, client, message):
            """
            Calls the check to validate whether it passes with the given conditions.
            
            Parameters
            ----------
            client : ``Client``
                The client who's received the message.
            message : ``Message``
                The received message.
            
            Returns
            -------
            passed : `bool`
                Whether the check passed.
            """
            guild = message.channel.guild
            if guild is None:
                return False
            
            if guild.permissions_for(message.author)>=self.permissions:
                return True
            
            return False
    
    class owner_or_has_guild_permissions(has_permissions):
        """
        Checks whether a message's author has the given permissions at the message's guild, or if it is the client's
        owner.
        
        Attributes
        ----------
        handler : `None` or `async-callable`
            An async callable what will be called when the check fails.
        permissions : ``Permission``
            The permission what the message's author should have at message's guild.
        """
        __slots__ = ('permissions', )
        async def __call__(self, client, message):
            """
            Calls the check to validate whether it passes with the given conditions.
            
            Parameters
            ----------
            client : ``Client``
                The client who's received the message.
            message : ``Message``
                The received message.
            
            Returns
            -------
            passed : `bool`
                Whether the check passed.
            """
            guild = message.channel.guild
            if guild is None:
                return False
            
            user = message.author
            
            if guild.permissions_for(user)>=self.permissions:
                return True
            
            if client.is_owner(user):
                return True
            
            return False
    
    class client_has_permissions(_check_base):
        """
        Checks whether a client has the given permissions at the message's channel.
        
        Attributes
        ----------
        handler : `None` or `async-callable`
            An async callable what will be called when the check fails.
        permissions : ``Permission``
            The permission what the client should have at message's channel.
        """
        __slots__ = ('permissions', )
        def __new__(cls, permissions, handler=None):
            """
            Creates a check, what will validate whether the a received message of a client passes the given condition.
            
            Parameters
            ----------
            permissions : ``Permission`` or `in` instance
                The permisison, what the client should have at the message's channel.
            handler : `None` or `async-callable` or instanceable to `async-callable`
                The handler to convert.
                
                If the handler is `async-callable` or if it would be instanced to it, then it should accept the
                following arguments:
                +-------------------+---------------------------+
                | Respective name   | Type                      |
                +===================+===========================+
                | client            | ``Client``                |
                +-------------------+---------------------------+
                | message           | ``Message``               |
                +-------------------+---------------------------+
                | command           | ``Command``               |
                +-------------------+---------------------------+
                | check             | ``_check_base`` instance  |
                +-------------------+---------------------------+
            
            Raises
            ------
            TypeError
                - `permissions` was not given as `int` instance.
                - If `handler` was given as an invalid type, or it accepts a bad amount of arguments.
            """
            permissions = _convert_permissions(permissions)
            handler = _convert_handler(handler)
            
            self = object.__new__(cls)
            self.permissions = permissions
            self.handler = handler
            return self
        
        async def __call__(self, client, message):
            """
            Calls the check to validate whether it passes with the given conditions.
            
            Parameters
            ----------
            client : ``Client``
                The client who's received the message.
            message : ``Message``
                The received message.
            
            Returns
            -------
            passed : `bool`
                Whether the check passed.
            """
            if message.channel.cached_permissions_for(client)>=self.permissions:
                return True
            
            return False
    
    class client_has_guild_permissions(_check_base):
        """
        Checks whether a client has the given permissions at the message's guild.
        
        Attributes
        ----------
        handler : `None` or `async-callable`
            An async callable what will be called when the check fails.
        permissions : ``Permission``
            The permission what the client should have at message's guild.
        """
        __slots__ = ('permissions', )
        def __new__(cls, permissions, handler=None):
            """
            Creates a check, what will validate whether the a received message of a client passes the given condition.
            
            Parameters
            ----------
            permissions : ``Permission`` or `in` instance
                The permisison, what the client should have at the message's guild.
            handler : `None` or `async-callable` or instanceable to `async-callable`
                The handler to convert.
                
                If the handler is `async-callable` or if it would be instanced to it, then it should accept the
                following arguments:
                +-------------------+---------------------------+
                | Respective name   | Type                      |
                +===================+===========================+
                | client            | ``Client``                |
                +-------------------+---------------------------+
                | message           | ``Message``               |
                +-------------------+---------------------------+
                | command           | ``Command``               |
                +-------------------+---------------------------+
                | check             | ``_check_base`` instance  |
                +-------------------+---------------------------+
            
            Raises
            ------
            TypeError
                - `permissions` was not given as `int` instance.
                - If `handler` was given as an invalid type, or it accepts a bad amount of arguments.
            """
            permissions = _convert_permissions(permissions)
            handler = _convert_handler(handler)
            
            self = object.__new__(cls)
            self.permissions = permissions
            self.handler = handler
            return self
        
        async def __call__(self, client, message):
            """
            Calls the check to validate whether it passes with the given conditions.
            
            Parameters
            ----------
            client : ``Client``
                The client who's received the message.
            message : ``Message``
                The received message.
            
            Returns
            -------
            passed : `bool`
                Whether the check passed.
            """
            guild = message.channel.guild
            if guild is None:
                return False
            
            if guild.cached_permissions_for(client)>=self.permissions:
                return True
            
            return False
    
    class is_guild(_check_base):
        """
        Checks whether the message was sent to the given guild.
        
        Attributes
        ----------
        handler : `None` or `async-callable`
            An async callable what will be called when the check fails.
        guild_id : `int`
            The respective guild's id.
        """
        __slots__ = ('guild_id', )
        def __new__(cls, guild, handler=None):
            """
            Creates a check, what will validate whether the a received message of a client passes the given condition.
            
            Parameters
            ----------
            guild : `str`, `int` or ``Guild``
                The guild where the message should be sent.
            handler : `None` or `async-callable` or instanceable to `async-callable`
                The handler to convert.
                
                If the handler is `async-callable` or if it would be instanced to it, then it should accept the
                following arguments:
                +-------------------+---------------------------+
                | Respective name   | Type                      |
                +===================+===========================+
                | client            | ``Client``                |
                +-------------------+---------------------------+
                | message           | ``Message``               |
                +-------------------+---------------------------+
                | command           | ``Command``               |
                +-------------------+---------------------------+
                | check             | ``_check_base`` instance  |
                +-------------------+---------------------------+
            
            Raises
            ------
            TypeError
                - If `guild` was not given neither as ``Guild``, `str` or `int` instance.
                - If `handler` was given as an invalid type, or it accepts a bad amount of arguments.
            ValueError
                If `guild` was given as `str` or as `int` instance, but not as a valid snowflake.
            """
            guild_id = instance_or_id_to_snowflake(guild, Guild)
            handler = _convert_handler(handler)
            
            self = object.__new__(cls)
            self.guild_id = guild_id
            self.handler = handler
            return self
        
        async def __call__(self, client, message):
            """
            Calls the check to validate whether it passes with the given conditions.
            
            Parameters
            ----------
            client : ``Client``
                The client who's received the message.
            message : ``Message``
                The received message.
            
            Returns
            -------
            passed : `bool`
                Whether the check passed.
            """
            guild = message.channel.guild
            if guild is None:
                return False
            
            if (guild.id==self.guild_id):
                return True
            
            return False
        
    class is_any_guild(_check_base):
        """
        Checks whether the message was sent to any of the given guilds.
        
        Attributes
        ----------
        handler : `None` or `async-callable`
            An async callable what will be called when the check fails.
        guild_ids : `set of `int`
            The respective guilds' ids.
        """
        __slots__ = ('guild_ids', )
        def __new__(cls, guilds, handler=None):
            """
            Creates a check, what will validate whether the a received message of a client passes the given condition.
            
            Parameters
            ----------
            guilds : `iterable` of (`str`, `int` or ``Guild``)
                Guilds to where the message should be sent.
            handler : `None` or `async-callable` or instanceable to `async-callable`
                The handler to convert.
                
                If the handler is `async-callable` or if it would be instanced to it, then it should accept the
                following arguments:
                +-------------------+---------------------------+
                | Respective name   | Type                      |
                +===================+===========================+
                | client            | ``Client``                |
                +-------------------+---------------------------+
                | message           | ``Message``               |
                +-------------------+---------------------------+
                | command           | ``Command``               |
                +-------------------+---------------------------+
                | check             | ``_check_base`` instance  |
                +-------------------+---------------------------+
            
            Raises
            ------
            TypeError
                - If `guilds` was not given as an `iterable`.
                - If an element of `guilds` was not given neither as ``Guild``, `str` or `int` instance.
                - If `handler` was given as an invalid type, or it accepts a bad amount of arguments.
            ValueError
                If an element of `guilds` was given as `str` or as `int` instance, but not as a valid snowflake.
            """
            guild_type = guilds.__class__
            if not hasattr(guild_type,'__iter__'):
                raise TypeError(f'`guilds` can be given as `iterable` of (`str`, `int` or `{Guild.__name__}`, got '
                    f'{guild_type.__name__}.')
            
            guild_ids_processed = set()
            for guild in guilds:
                guild_id = instance_or_id_to_snowflake(guild, Guild)
                guild_ids_processed.add(guild_id)
            
            handler = _convert_handler(handler)
            
            self = object.__new__(cls)
            self.guild_ids = guild_ids_processed
            self.handler = handler
            return self
        
        async def __call__(self, client, message):
            """
            Calls the check to validate whether it passes with the given conditions.
            
            Parameters
            ----------
            client : ``Client``
                The client who's received the message.
            message : ``Message``
                The received message.
            
            Returns
            -------
            passed : `bool`
                Whether the check passed.
            """
            guild = message.channel.guild
            if guild is None:
                return False
            
            if (guild.id in self.guild_ids):
                return True
            
            return False
    
    class custom(_check_base):
        """
        Checks whether the message and client passes the given custom condition.
        
        Attributes
        ----------
        handler : `None` or `async-callable`
            An async callable what will be called when the check fails.
        function : `callable`
            The custom check's function.
        """
        __slots__ = ('_is_async', 'function')
        def __new__(cls, function, handler=None):
            """
            Creates a check, what will validate whether the a received message of a client passes the given condition.
            
            Parameters
            ----------
            function : `callable`
                The custom check what should pass.
            handler : `None` or `async-callable` or instanceable to `async-callable`
                The handler to convert.
                
                If the handler is `async-callable` or if it would be instanced to it, then it should accept the
                following arguments:
                +-------------------+---------------------------+
                | Respective name   | Type                      |
                +===================+===========================+
                | client            | ``Client``                |
                +-------------------+---------------------------+
                | message           | ``Message``               |
                +-------------------+---------------------------+
                | command           | ``Command``               |
                +-------------------+---------------------------+
                | check             | ``_check_base`` instance  |
                +-------------------+---------------------------+
            
            Raises
            ------
            TypeError
                - If `function` was not given as an `callable`.
                - `function` accepts more or less non reserved positional non default arguments.
                - If `handler` was given as an invalid type, or it accepts a bad amount of arguments.
            
            Notes
            -----
            Only `int` instances are evaluated to boolean.
            """
            analyzer = CallableAnalyzer(function)
            non_reserved_positional_argument_count = analyzer.get_non_reserved_positional_argument_count()
            if  non_reserved_positional_argument_count != 2:
                raise TypeError(f'The passed function: {function!r} should have accept `2` non reserved, positional, '
                    f'non default arguments, meanwhile it accepts `{non_reserved_positional_argument_count}`.')
            
            is_async = analyzer.is_async()
            handler = _convert_handler(handler)
            
            self = object.__new__(cls)
            self.function = function
            self._is_async = is_async
            self.handler = handler
            return self
        
        async def __call__(self, client, message):
            """
            Calls the check to validate whether it passes with the given conditions.
            
            Parameters
            ----------
            client : ``Client``
                The client who's received the message.
            message : ``Message``
                The received message.
            
            Returns
            -------
            passed : `bool`
                Whether the check passed.
            """
            try:
                result = self.function(client, message)
                if self._is_async:
                    result = await result
            except BaseException as err:
                Task(client.events.error(client,repr(self),err), KOKORO)
                return False
            
            if result is None:
                return False
            
            if isinstance(result, int) and result:
                return True
            
            return False
    
    class is_channel(_check_base):
        """
        Checks whether the message was sent to the given channel.
        
        Attributes
        ----------
        handler : `None` or `async-callable`
            An async callable what will be called when the check fails.
        channel_id : `int`
            The respective channel's id.
        """
        __slots__ = ('channel_id', )
        def __new__(cls, channel, handler=None):
            """
            Creates a check, what will validate whether the a received message of a client passes the given condition.
            
            Parameters
            ----------
            channel : `str`, `int` or ``ChannelBase``
                The channel where the message should be sent.
            handler : `None` or `async-callable` or instanceable to `async-callable`
                The handler to convert.
                
                If the handler is `async-callable` or if it would be instanced to it, then it should accept the
                following arguments:
                +-------------------+---------------------------+
                | Respective name   | Type                      |
                +===================+===========================+
                | client            | ``Client``                |
                +-------------------+---------------------------+
                | message           | ``Message``               |
                +-------------------+---------------------------+
                | command           | ``Command``               |
                +-------------------+---------------------------+
                | check             | ``_check_base`` instance  |
                +-------------------+---------------------------+
            
            Raises
            ------
            TypeError
                - If `channel` was not given neither as ``ChannelBase``, `str` or `int` instance.
                - If `handler` was given as an invalid type, or it accepts a bad amount of arguments.
            ValueError
                If `channel` was given as `str` or as `int` instance, but not as a valid snowflake.
            """
            channel_id = instance_or_id_to_snowflake(channel, ChannelBase)
            handler = _convert_handler(handler)
            
            self = object.__new__(cls)
            self.channel_id = channel_id
            self.handler = handler
            return self
        
        async def __call__(self, client, message):
            """
            Calls the check to validate whether it passes with the given conditions.
            
            Parameters
            ----------
            client : ``Client``
                The client who's received the message.
            message : ``Message``
                The received message.
            
            Returns
            -------
            passed : `bool`
                Whether the check passed.
            """
            if (message.channel.id==self.channel_id):
                return True
            
            return False
        
    class is_any_channel(_check_base):
        """
        Checks whether the message was sent to any of the given channels.
        
        Attributes
        ----------
        handler : `None` or `async-callable`
            An async callable what will be called when the check fails.
        channel_ids : `set of `int`
            The respective channels' ids.
        """
        __slots__ = ('channel_ids', )
        def __new__(cls, channels, handler=None):
            """
            Creates a check, what will validate whether the a received message of a client passes the given condition.
            
            Parameters
            ----------
            channels : `iterable` of (`str`, `int` or ``ChannelBase``)
                Channels to where the message should be sent.
            handler : `None` or `async-callable` or instanceable to `async-callable`
                The handler to convert.
                
                If the handler is `async-callable` or if it would be instanced to it, then it should accept the
                following arguments:
                +-------------------+---------------------------+
                | Respective name   | Type                      |
                +===================+===========================+
                | client            | ``Client``                |
                +-------------------+---------------------------+
                | message           | ``Message``               |
                +-------------------+---------------------------+
                | command           | ``Command``               |
                +-------------------+---------------------------+
                | check             | ``_check_base`` instance  |
                +-------------------+---------------------------+
            
            Raises
            ------
            TypeError
                - If `channels` was not given as an `iterable`.
                - If an element of `channels` was not given neither as ``ChannelBase``, `str` or `int` instance.
                - If `handler` was given as an invalid type, or it accepts a bad amount of arguments.
            ValueError
                If an element of `channels` was given as `str` or as `int` instance, but not as a valid snowflake.
            """
            channels_type = channels.__class__
            if not hasattr(channels_type,'__iter__'):
                raise TypeError(f'`channels` can be given as `iterable` of (`str`, `int` or `{ChannelBase.__name__}`, '
                    f'got {channels_type.__name__}.')
            
            channel_ids_processed = set()
            for channel in channels:
                channel_id = instance_or_id_to_snowflake(channel, ChannelBase)
                channel_ids_processed.add(channel_id)
            
            handler = _convert_handler(handler)
            
            self = object.__new__(cls)
            self.channel_ids = channel_ids_processed
            self.handler = handler
            return self
        
        async def __call__(self, client, message):
            """
            Calls the check to validate whether it passes with the given conditions.
            
            Parameters
            ----------
            client : ``Client``
                The client who's received the message.
            message : ``Message``
                The received message.
            
            Returns
            -------
            passed : `bool`
                Whether the check passed.
            """
            if (message.channel.id in self.channel_ids):
                return True
            
            return False

from .command.checks import validate_checks

class Category(object):
    """
    Represents a category of a ``CommandProcesser.md``.
    
    Categories can be used to apply checks for their commands and for using a global check failure handler for each
    of them as well.
    
    Attributes
    ----------
    _checks : `None` or (`list` of ``_check_base`` instances)
        The internal slot used by the ``.checks`` property. Defaults to `None`.
    commands : `sortedist` of ``Command``
        Sortedlist storing the category's commands.
    description : `Any`
        Optional description for the category.
    name : `None` or `str`
        The name of the category. Only a command processer's default category can have it's name as `None`.
    """
    __slots__ = ('_checks', 'commands', 'description', 'name', )
    
    def __new__(cls, name, checks_=None, description=None):
        """
        Creates a new category with the given parameters.
        
        Parameters
        ----------
        name : `None` or `str`
            The name of the category. Only a command processer's default category can have it's name as `None`.
        checks_ : `None` or (`iterable` of ``_check_base`` instances), Optional
            Checks to define in which circumstances a command should be called.
        description : `Any`
            Optional description for the category. Defaults to `None`.
        
        Returns
        -------
        self : ``Category``
        
        Raises
        ------
        TypeError
            If `checks_` was not given as `None` or as `iterable` of ``_check_base`` instances.
        """
        checks_processed = validate_checks(checks_)
        
        if (description is not None) and isinstance(description,str):
            description=normalize_description(description)
        
        self=object.__new__(cls)
        self.name=name
        self.commands=sortedlist()
        self._checks = checks_processed
        self.description=description
        return self
    
    def _get_checks(self):
        checks = self._checks
        if (checks is not None):
            checks = checks.copy()
        
        return checks
    
    def _set_checks(self, checks_):
        self._checks = validate_checks(checks_)
    
    def _del_checks(self):
        self._checks = None
    
    checks = property(_get_checks, _set_checks, _del_checks)
    del _get_checks, _set_checks, _del_checks
    
    if (__new__.__doc__ is not None):
        checks.__doc__ = ("""
        Get-set-del property for accessing the checks of the ``Category``.
        
        When using it is get property returns the checks of the category, what can be `None` or `list` of
        ``_check_base`` instances.
        
        When setting it, accepts `None` or an `iterable` of ``_check_base`` instances. Raises `TypeError` if invalid
        type or element type is given.
        
        By deleting it removes the command's checks.
        """)
    
    async def run_checks(self, client, message):
        """
        Runs all the checks of the category and returns whtether every of them passed.
        
        Parameters
        ----------
        client : ``Client``
            The client with what the checks will be called.
        message : ``Message``
            The message with what the checks will be called.
        
        result : `int`
            Returns an identificator number depending how the command execution went.
            
            Possible values:
            +---------------------------+-------+
            | Respective name           |Value  |
            +===========================+=======+
            | COMMAND_CHECKS_FAILED     | 0     |
            +---------------------------+-------+
            | COMMAND_CHECKS_SUCCEEDED  | 1     |
            +---------------------------+-------+
        """
        checks=self._checks
        if (checks is not None):
            for check in checks:
                if await check(client, message):
                    continue
                
                return COMMAND_CHECKS_FAILED
        
        return COMMAND_CHECKS_SUCCEEDED
    
    def __gt__(self, other):
        """Returns whether this category's name is greater than the other's"""
        self_name=self.name
        other_name=other.name
        
        if self_name is None:
##            if other_name is None:
##                return False
##            else:
##                return False
            return False
        else:
            if other_name is None:
                return True
            else:
                return (self_name>other_name)
    
    def __lt__(self, other):
        """Returns whether this category's name is less than the other's"""
        self_name=self.name
        other_name=other.name
        
        if self_name is None:
            if other_name is None:
                return False
            else:
                return True
        else:
            if other_name is None:
                return False
            else:
                return (self_name<=other_name)
    
    def __iter__(self):
        """Returns an iterator over the category's commands."""
        return iter(self.commands)
    
    def __reversed__(self):
        """Returns a reversed iterator over the category's commands."""
        return reversed(self.commands)
    
    def __len__(self):
        """Returns the amount of commands of the category."""
        return len(self.commands)
    
    def __repr__(self):
        """Returns the representation of the category."""
        result = [
            '<',
            self.__class__.__name__,
                ]
        name=self.name
        if (name is not None):
            result.append(' ')
            result.append(name)
            
        result.append(' length=')
        result.append(repr(len(self.commands)))
        result.append(', checks=')
        result.append(repr(self._checks))
        result.append('>')
        
        return ''.join(result)

class CommandProcesser(EventWaitforBase):
    """
    A predefined class to help out the bot devs with an already defined `message_create` event.

    The class is part of the wrapper's `commands` extension, what can be setupped, with ``setup_ext_commands``
    function after importing it from the extension. ``setup_ext_commands`` adds other event handlers to the client
    as well.
    
    Flow
    ----
    When a command processer is called, the following steps are done:
    
    - `waitfor`
        Command processer allows you to wait for a message at a channel or at a guild. If any message is received
        at a waited entity, then all the waiters are ensured with the client and with the received ``Message`` object.
        
        > At this point no bot messages, or missing permissions are filtered out.
    
    - `commands`
        First bot messages are filtered out, then the channels, where the client cannot send messages
        After the message's content is parsed out to `3` parts if possible: `prefix, `command-name` and `content`.
        If a ``Command`` is added with the parsed `command-name` name or alias, then it will be ensured.
        
        If the command returns `0`, the command processer will act, like there is no command iwth the given name.
        
    - `invalid_command`
        If `prefix` is valid, but the command not exists (or it returned `0`) will be called (if set) with `4`
        arguments:
        
        +-------------------+---------------+
        | Respective name   | Type          |
        +===================+===============+
        | client            | ``Client``    |
        +-------------------+---------------+
        | message           | ``Message``   |
        +-------------------+---------------+
        | command           | `str`         |
        +-------------------+---------------+
        | content           | `str`         |
        +-------------------+---------------+
    
    - `mention_prefix`
        If a message starts with the mention of the client, then the command procsser will act, like it was a command
        call. Although if no command exists with the given name, then `invalid-command` will not be called, instead
        will move on the next step.
    
    - `default_event`
        If the received message was not a comamnd call, then this event is ensured (if set) with 2 arguments:
        
        +-------------------+---------------+
        | Respective name   | Type          |
        +===================+===============+
        | client            | ``Client``    |
        +-------------------+---------------+
        | message           | ``Message``   |
        +-------------------+---------------+
    
    - `command_error`
        If a command call was executed by the `commands` or by the `mention_prefix` part and the command raised, then
        `command_error` is called with the details:
        
        +-------------------+-------------------+
        | Respective name   | Type              |
        +===================+===================+
        | client            | ``Client``        |
        +-------------------+-------------------+
        | message           | ``Message``       |
        +-------------------+-------------------+
        | command           | ``Command``       |
        +-------------------+-------------------+
        | content           | `str`             |
        +-------------------+-------------------+
        | err               | ``BaseException`` |
        +-------------------+-------------------+
    
    Attributes
    ----------
    waitfors : `WeakValueDictionary` of (``DiscordEntity``, `asnyc-callable`) items
        Container to store the entities where message is expected to be sent and their waiters.
    _command_error : `None` or `async-callable`
        Called when execution of a command raised. Internal slot used by the ``.command_error`` property.
    _command_error_checks : `None` or `list` of ``_check_base``
        Checks to deside whether ``._command_error`` should be called. Internal slot used by the
        ``.command_error_checks`` property.
    _default_category_name : `None` or `str`
        The command processser's default category's name.
    _default_event : `None` or `async-callable`
        Called when no command execution took place. Internal slot used by the ``.default_event`` property.
    _default_event_checks : `None` or `list` of ``_check_base``
        Checks to deside whether ``._default_event`` should be called. Internal slot used by the
        ``.default_event_checks`` property.
    _ignorecase : `bool`
        Whether prefix is case insensitive.
    _invalid_command : `None` or `async_callable`
        Calleed when there is no command with the given name. Internal slot used by the ``.invalid_command`` property.
    _invalid_command_checks : `None` or `list` of ``_check_base``
        Checks to deside whether ``._invalid_command`` should be called. Internal slot used by the
        ``.invalid_command_checks`` property.
    categories : `sortedlist` of ``Category``
        The command processer's categories.
    commands : `dict` of (`str`, `Command`) items
        Command `alternaetive-name` - ``Command`` relation used to lookup commands.
        
        > `Command_processer.commands` is not the same as `Client.commands` !
    
    get_prefix_for : `callable`
        A function to get the client's preffered prefix for the given message.
        
        ``.get_prefix_for`` acccepts only `1` argument:
        +-------------------+---------------+
        | Respective name   | Type          |
        +===================+===============+
        | message           | ``Message``   |
        +-------------------+---------------+
        
        > Note, that if the ``CommandProcesser``-s `prefix` was set as an `async-callable`, then ``get_prefix_for``
        > will return an `awaitable` as well.
    
    mention_prefix : `bool`
        Whether the command processer accepts the respective client's mention as an alternative prefix.
    prefix : `Any`
        The passed prefix at creation or at update.
    prefixfilter : `async-callable`
        A generated function to check whether a message's content starts with the command processer's `prefix`.
    
    Class Attributes
    ----------------
    __event_name__ : `str` = 'message_create'
        Tells for the ``EventDescriptor`` that ``CommandProcesser`` is a `message_create` event handler.
    SUPPORTED_TYPES : `tuple` (``Command``,)
        Tells to ``eventlist`` what exact types the ``CommandProcesser`` accepts.
    """
    __slots__ = ('_command_error', '_command_error_checks', '_default_category_name', '_default_event',
        '_default_event_checks', '_ignorecase', '_invalid_command', '_invalid_command_checks', 'categories',
        'commands', 'get_prefix_for', 'mention_prefix', 'prefix', 'prefixfilter')
    
    __event_name__ = 'message_create'
    
    SUPPORTED_TYPES = (Command, )
    
    def __new__(cls, prefix, ignorecase=True, mention_prefix=True, default_category_name=None):
        """
        Creates an ``CommandProcesser`` instance.
        
        Parameters
        ----------
        prefix :  `str`, ((tuple`, `list`) of `str`), `callable`
            Prefix for the command processer.
            
            Can be given as normal or as `async` `callable` as well, what should accept `1` argument:
            +-------------------+---------------+
            | Respective name   | Type          |
            +===================+===============+
            | message           | ``Message``   |
            +-------------------+---------------+
        
        ignorecase : `bool`, Optional
            Whether prefix is case insensitive. Defaults to `True`.
        mention_prefix : `bool`, Optional
            Whether the command processer accepts the respective client's mention as an alternative prefix. Defaults
            to `True`.
        default_category_name : `None` or `str`, Optional
            The command processser's default category's name. Defaults to `None`.
        
        Raises
        ------
        TypeError
            - If `default_category_name` was not passed as `None`, or as `str` instance.
            - If `prefix` was given as a `callable`, but accepts bad amount of arguments.
            - If `prefix` was given as `tuple`or `list`, but contains a non `str`.
            - If `prefix` was not given as `str`, (tuple`, `list`) of `str` or as `callable`.
        ValueError
            - If `prefix` was given as an empty `str`.
        Returns
        -------
        self : ``CommandProcesser``
        """
        if (default_category_name is not None):
            default_category_name_type = default_category_name.__class__
            if default_category_name_type is str:
                pass
            elif issubclass(default_category_name_type, str):
                default_category_name = str(default_category_name)
            else:
                raise TypeError(f'`default_category_name` should have been passed as `None`, or as `str` instance, '
                    f'got {default_category_name.__name__}.')
            
            if not default_category_name:
                default_category_name = None
        
        self = object.__new__(cls)
        self._command_error = None
        self._command_error_checks = None
        self._default_event = None
        self._default_event_checks = None
        self._invalid_command = None
        self._invalid_command_checks = None
        self.mention_prefix=mention_prefix
        self.commands={}
        self.update_prefix(prefix,ignorecase)
        self._ignorecase=ignorecase
        
        self._default_category_name=default_category_name
        categories=sortedlist()
        self.categories=categories
        categories.add(Category(default_category_name))
        return self
    
    def get_category(self, category_name):
        """
        Returns the category for the given name. If the name is passed as `None`, then will return the default category
        of the command processer.
        
        Returns `None` if there is no category with the given name.
        
        Parameters
        ---------
        category_name : `str`, `None`
        
        Returns
        -------
        category : `None`, ``Category``
        
        Raises
        ------
        TypeError
            If `category_name` was not given as `None` and neither as `str` instance.
        """
        # category name can be None, but when we wanna use `.get` we need to
        # use compareable datatypes, so whenever we get we need to convert
        # `None` to empty `str` at every case
        if category_name is None:
            category_name = self._default_category_name
            if category_name is None:
                category_name = ''
        else:
            category_name_type = category_name.__class__
            if category_name_type is str:
                pass
            elif issubclass(category_name_type, str):
                category_name = str(category_name)
            else:
                raise TypeError(f'`category_name` can be given as `None` or as `instance`, got '
                    f'{category_name_type.__class__}.')
            
            if not category_name:
                category_name = self._default_category_name
                if category_name is None:
                    category_name = ''
        
        return self.categories.get(category_name, key=self._get_category_key)
    
    def get_default_category(self):
        """
        Returns the command processer's default category.
        
        Returns
        -------
        category : ``Category``
        """
        category_name = self._default_category_name
        if category_name is None:
            category_name = ''
        return self.categories.get(category_name, key=self._get_category_key)
    
    @staticmethod
    def _get_category_key(category):
        """
        Used as a key, when searching a category for a specific name at `.categories`.
        """
        name = category.name
        if name is None:
            return ''
        
        return name
    
    def _get_default_category_name(self):
        return self._default_category_name
    
    def _set_default_category_name(self, default_category_name):
        if (default_category_name is not None):
            default_category_name_type = default_category_name.__class__
            if default_category_name_type is str:
                pass
            elif issubclass(default_category_name_type, str):
                default_category_name = str(default_category_name)
            else:
                raise TypeError(f'`category_name` can be given as `None` or as `instance`, got '
                    f'{default_category_name_type.__class__}.')
            
            if not default_category_name:
                default_category_name = None
        
        # if both is same, dont do anything
        actual_default_category_name = self._default_category_name
        if default_category_name is None:
            if actual_default_category_name is None:
                return
        else:
            if (actual_default_category_name is not None) and (default_category_name==actual_default_category_name):
                return
        
        other_category = self.get_category(default_category_name)
        if (other_category is not None):
            raise ValueError(f'There is already a category added with name: `{default_category_name!r}`.')
        
        default_category = self.get_category(actual_default_category_name)
        default_category.name = default_category_name
        self.categories.resort()
        self._default_category_name = default_category_name
    
    default_category_name = property(_get_default_category_name,_set_default_category_name)
    del _get_default_category_name, _set_default_category_name
    
    if (__new__.__doc__ is not None):
        default_category_name.__doc__ = ("""
        A get-set property for accessing or changing the command processer's dfault category's name.
        
        Accepts and returns `None`, or `str` instance.
        
        > If given as not `None` or `str` instance, raises `TypeError`.
        """)
    
    def create_category(self, name, checks=None, description=None):
        """
        Creates a category with the given parameters.
        
        Parameters
        ----------
        name : `str`
            The name of the category. Only a command processer's default category can have it's name as `None`.
        checks : `None` or (`iterable` of ``_check_base`` instances), Optional
            Checks to define in which circumstances a command should be called.
        description : `Any`
            Optional description for the category. Defaults to `None`.
        
        Returns
        -------
        category : ``Category``
        
        Raises
        ------
        TypeError
            If `checks_` was not given as `None` or as `iterable` of ``_check_base`` instances.
        ValueError
            - If a category exists with the given name.
        """
        category = self.get_category(name)
        if (category is not None):
            raise ValueError(f'There is already a category added with that name: `{name!r}`')
        
        category=Category(name,checks,description)
        self.categories.add(category)
        return category
    
    def delete_category(self, category):
        """
        Deletes the category of the command processer.
        
        Parameters
        ----------
        category : ``Category``, `str`
            The category or the category's name to remove.
        
        Raises
        ------
        TypeError
            If `category` was not given as `None`, ``Category` or as `str` instance.
        ValueError
            If the default category would be deleted.
        """
        if category is None:
            raise ValueError('Default category cannot be deleted.')
        
        category_type = category.__class__
        if category_type is Category:
            category_name = category.name
        elif category_type is str:
            category_name = category
        elif issubclass(category_type, str):
            category_name = str(category)
        else:
            raise TypeError(f'Expected type `str` or `{Category.__class__.__name__} as `category`, got '
                f'{category_type.__name__}.')
        
        category = self.categories.pop(category_name, key=self._get_category_key)
        if category is None:
            return
        
        commands = self.commands
        for command in category.commands:
            alters = command._alters
            for name in alters:
                other_command = commands.get(name)
                if other_command is command:
                    del commands[name]
    
    def update_prefix(self, prefix, ignorecase=None):
        """
        Updates the command processer's prefix.
        
        Parameters
        ----------
        prefix :  `str`, ((tuple`, `list`) of `str`), `callable`
            Prefix for the command processer.
            
            Can be given as normal or as `async` `callable` as well, what should accept `1` argument:
            +-------------------+---------------+
            | Respective name   | Type          |
            +===================+===============+
            | message           | ``Message``   |
            +-------------------+---------------+
        
        ignorecase : `bool`, Optional
            Whether prefix is case insensitive. Defaults to the command processer's.
        
        Raises
        ------
        TypeError
            - If `prefix` was given as a `callable`, but accepts bad amount of arguments.
            - If `prefix` was given as `tuple`or `list`, but contains a non `str`.
            - If `prefix` was not given as `str`, (tuple`, `list`) of `str` or as `callable`.
        ValueError
            - If `prefix` was given as an empty `str`.
        """
        if ignorecase is None:
            ignorecase = self._ignorecase
        if ignorecase:
            flag = re.I
        else:
            flag = 0
        
        while True:
            if callable(prefix):
                analyzed = CallableAnalyzer(prefix)
                non_reserved_positional_argument_count = analyzed.get_non_reserved_positional_argument_count()
                if non_reserved_positional_argument_count != 1:
                    raise TypeError(f'If `prefix` is given as a `callable`, got {callable!r}, then it should accept '
                        'only `1` non reserved position argument, meanwhile it accepts: '
                        f'`{non_reserved_positional_argument_count}`.')
                
                if analyzed.is_async():
                    async def prefixfilter(message):
                        practical_prefix = await prefix(message)
                        if re.match(re.escape(practical_prefix),message.content,flag) is None:
                            return
                        result = COMMAND_RP.match(message.content,len(practical_prefix))
                        if result is None:
                            return
                        return result.groups()
                else:
                    async def prefixfilter(message):
                        practical_prefix = prefix(message)
                        if re.match(re.escape(practical_prefix),message.content,flag) is None:
                            return
                        result = COMMAND_RP.match(message.content,len(practical_prefix))
                        if result is None:
                            return
                        return result.groups()
                
                get_prefix_for = prefix
                break
            
            if type(prefix) is str:
                if not prefix:
                    raise ValueError('Prefix cannot be passed as empty string.')
                
                PREFIX_RP=re.compile(re.escape(prefix),flag)
                def get_prefix_for(message):
                    return prefix
            
            elif isinstance(prefix,(list,tuple)):
                if not prefix:
                    raise ValueError(f'Prefix fed as empty {prefix.__class__.__name__}: {prefix!r}')
                
                for prefix_ in prefix:
                    if type(prefix_) is not str:
                        raise TypeError(f'Prefix can be only callable, str or tuple/list type of str, got {prefix_!r}')
                    
                    if not prefix_:
                        raise ValueError('Prefix cannot be passed as empty string.')
                
                PREFIX_RP=re.compile("|".join(re.escape(prefix_) for prefix_ in prefix),flag)
                practical_prefix = prefix[0]
                
                def get_prefix_for(message):
                    result=PREFIX_RP.match(message.content)
                    if result is None:
                        return practical_prefix
                    else:
                        return result.group(0)
            else:
                raise TypeError(f'Prefix can be only `callable`, `str` or `tuple` / `list` of `str` instances,  got '
                    f'{prefix.__class__.__name__}.')
            
            async def prefixfilter(message):
                content = message.content
                result=PREFIX_RP.match(content)
                if result is None:
                    return
                result=COMMAND_RP.match(content,result.end())
                if result is None:
                    return
                return result.groups()
            
            break
        
        self.prefix = prefix
        self.prefixfilter = prefixfilter
        self.get_prefix_for = get_prefix_for
        self._ignorecase = ignorecase
    
    def __setevent__(self, func, name, description=None, aliases=None, category=None, checks=None, parser_failure_handler=None):
        """
        Method used to add commands to the command procseer.
        
        Parameters
        ---------
        func : ``Command``, `async-callable`, instanceable to `async-callable`
            The function to be added as a command.
        name : `None` or `str`
            The command's name.
            
            There are `3` magic command names, which are the following:
            - `default_event`
            - `invalid_command`
            - `command_error`
            
            If any of these is given as `name`, then the given `func` with it's `checks` will be added as their
            property representation.
            
            > Giving `func` as ``Command`` instance is always checked and added first tho.
        
        description : `Any`, Optional
            Description for the command. Defaults to `None`.
        aliases : `None` or (`iterable` of `str`)
            Aliases for the command. Defaults to `None`
        category : `None`, `str`, ``Category``
            The category for the command. Defaults to `None`
        checks : `None` or (`iterable` of ``_check_base`` instances)
            Checks to deside in which circumstances the command should be called. Defaults to `None`.
        
        parser_failure_handler : `None` or `async-callable`
            Called when the command uses a parser to parse it's arguments, but it cannot parse out all the required
            ones. Defaults to `None`.
            
            If given as an `async-callable`, then it should accept 5 arguments:
            
            +-----------------------+-------------------+
            | Respective name       | Type              |
            +=======================+===================+
            | client                | ``Client``        |
            +-----------------------+-------------------+
            | message               | ``Message``       |
            +-----------------------+-------------------+
            | command               | ``Command``       |
            +-----------------------+-------------------+
            | content               | `str`             |
            +-----------------------+-------------------+
            | args                  | `list` of `Any`   |
            +-----------------------+-------------------+
        
        returns
        -------
        func : ``Command``, `async-callable`
             ``Command`` instance, if it was created from the given `func`.
         
        Raises
        ------
        TypeError
            - `aliases` were not passed as `None` or as `iterable` of `str`.
            - `category` was not given as `None, `str`, or as ``Category`` instance.
            - If `checks_` was not given as `None` or as `iterable` of ``_check_base`` instances.
        ValueError
            - If `category` was given as ``Category`` instance and the command processer already has a category
                with the same name as the `category`'s.
            - If the added command's `.name` would overwrite an alias of an other command.
            - If the added command would overwrite more than `1` already added command.
        """
        if type(func) is Command:
            self._add_command(func)
            return func
        
        if (name is not None):
            # called every time, but only if every other fails
            if name == 'default_event':
                func = check_argcount_and_convert(func, 2, '`default_event` expects 2 arguments (client, '
                    'message).')
                checks_processed = validate_checks(checks)
                self._default_event = func
                self._default_event_checks = checks_processed
                return func
            
            if name == 'command_error':
                func = check_argcount_and_convert(func, 5, '`invalid_command` expected 5 arguments (client, message, '
                    'command, content, exception).')
                checks_processed = validate_checks(checks)
                self._command_error = func
                self._command_error_checks = checks_processed
                return func
            
            # called when user used bad command after the preset prefix, called if a command fails
            if name == 'invalid_command':
                func = check_argcount_and_convert(func, 4, '`invalid_command` expected 4 arguments (client, message, '
                    'command, content).')
                checks_processed = validate_checks(checks)
                self._invalid_command = func
                self._invalid_command_checks = checks_processed
                return func
        
        # called first
        
        command = Command(func, name, description, aliases, category, checks, parser_failure_handler)
        self._add_command(command)
        return command
        
    def __setevent_from_class__(self, klass):
        """
        Breaks down the given class to it's class attrbiutes and tries to add it as a command.
        
        Parameters
        ----------
        klass : `type`
            The class, from what's attributes the command will be created.
            
            The expected attrbiutes of the given `klass` are the following:
            - name : `str` or `None`
                If was not defined, or was defined as `None`, the classe's name will be used.
            - command : `async-callable`
                If no `command` attribute was defined, then a attribute of the `name`'s value be checked as well.
            - description : `Any`
                If no description was provided, then the classe's `.__doc__` will be picked up.
            - aliases : `None` or (`iterable` of str`)
            - category : `None`, ``Category`` or `str`
            - checks : `None` or (`iterable` of ``_check_base``)
                If no checks were provided, then the classe's `.checks_` attribute will be checked as well.
            - parser_failure_handler : `None` or `async-callable`
        
        Returns
        -------
        command : ``Command``
            The created command.
        
        Raises
        ------
        TypeError
            - If `klass` was not given as `type` instance.
            - `aliases` were not passed as `None` or as `iterable` of `str`.
            - `category` was not given as `None, `str`, or as ``Category`` instance.
            - If `checks` was not given as `None` or as `iterable` of ``_check_base`` instances.
        ValueError
            - If `.command` attribute is missing of the class.
        """
        command = Command.from_class(klass)
        self._add_command(command)
        return command
    
    def _add_command(self, command):
        """
        Adds the given command to the command processer.
        
        Raises
        ------
        ValueError
            - If `category` was given as ``Category`` instance and the command processer already has a category
                with the same name as the `category`'s.
            - If the added command's `.name` would overwrite an alias of an other command.
            - If the added command would overwrite more than `1` already added command.
        """
        category = command.category
        if (category is not None):
            if self.get_category(category.name) is not category:
                raise ValueError(f'The passed `{Category.__name__}` object is not owned; `{category!r}`.')
            category_added = True
        
        else:
            category_hint = command._category_hint
            if category_hint is None:
                category_hint=self._default_category_name
            
            category=self.get_category(category_hint)
            if category is None:
                category=Category(category_hint)
                category_added = False
            else:
                category_added = True
            
            command.category = category
        
        commands=self.commands
        name=command.name
        
        would_overwrite = commands.get(name)
        if (would_overwrite is not None) and (would_overwrite.name!=name):
            raise ValueError(f'The command would overwrite an alias of an another one: `{would_overwrite}`.'
                'If you intend to overwrite an another command please overwrite it with it\'s default name.')
        
        alters=command._alters
        for alter in alters:
            try:
                overwrites=commands[alter]
            except KeyError:
                continue
            
            if overwrites is would_overwrite:
                continue
            
            error_message_parts = [
                'Alter `',
                repr(alter),
                '` would overwrite an other command; `',
                repr(overwrites),
                '`.',
                    ]
            
            if (would_overwrite is not None):
                error_message_parts.append(' The command already overwrites an another one with the same name: `')
                error_message_parts.append(repr(would_overwrite))
                error_message_parts.append('`.')
            
            raise ValueError(''.join(error_message_parts))
        
        if (would_overwrite is not None):
            alters = would_overwrite._alters
            for alter in alters:
                if commands[alter] is would_overwrite:
                    try:
                        del commands[alter]
                    except KeyError:
                        pass
            
            category=would_overwrite.category
            if (category is not None):
                category.commands.remove(would_overwrite)
            
        # If everything is correct check for category, create it if needed,
        # add to it. Then add to the commands as well with it's aliases ofc.
        
        category.commands.add(command)
        if not category_added:
            self.categories.add(category)
        
        # Alters contain `command.name` as well, so skip that case.
        alters = command._alters
        for alter in alters:
            commands[alter]=command
    
    def __delevent__(self, func, name, **kwargs):
        """
        A method to remove a command by itself, by it's function and name conbination if defined.
        
        If `func` is given as type ``Command`` and `name` is given as 1 of it's aliases, then the method removes only
        that specified alias.
        
        Parameters
        ----------
        func : ``Command``, `async-callable` or instanceable to `async-callable`
            The command to remove.
        name : `None` or `str`
            The command's name to remove.
        **kwargs : Keyword Arguments
            Other keyword only arguments are ignored.
        
        Raises
        ------
        TypeError
            - If `name` was not given as `None` or as `str` instance.
            - If ``func` was not given as type ``Command`` meanwhile `name` was given as `None`.
            - If `name` was given as one of `default_event`, `invalid_command`, `command_error`, but the command
                processer's respective attribute is different than the given `func`.
        ValueError
            - If `func` was given as type ``Command`` and `name` was not given as `None`, neitehr as 1 of it's aliases.
            _ If `func` was given as type ``Command`` there is no command added with the given `name`.
            - If `func` was given as type ``Command``, but the added command with the given `name` is different.
            - If `func` was not given type ``Command`` and the given `name` is not a name of a command of the command
                processer.
            - If `func` was not given as type ``Command`` and the command processer's command'd function with the given
                `name` is different from the given `func`.
        """
        if (name is not None):
            name_type = name.__class__
            if name_type is str:
                pass
            elif issubclass(name_type, str):
                name = str(name)
            else:
                raise TypeError(f'`name` can be `None` or `str` instance, got {name_type.__name__}.')
        
        if type(func) is Command:
            commands = self.commands
            if (name is None):
                name_alters = None
            else:
                name_alters = generate_alters_for(name)
                name = name_alters[0]
            
            if (name is None) or (name==func.name):
                found_alters = []
                
                for alter in func._alters:
                    try:
                        command = commands[alter]
                    except KeyError:
                        pass
                    else:
                        if command is func:
                            found_alters.append(name)
                
                if not found_alters:
                    raise ValueError(f'The passed command `{func!r}` is not added with any of it\'s own names as a '
                        f'command.')
                
                for alter in found_alters:
                    try:
                        del commands[alter]
                    except KeyError:
                        pass
                
                category = func.category
                if (category is not None):
                    category.commands.remove(func)
                
                return
            
            aliases = func.aliases
            if (aliases is None):
                raise ValueError(f'The passed name `{name!r}` is not the name, neither an alias of the command '
                    f'`{func!r}`.')
            
            if name not in aliases:
                raise ValueError(f'The passed name `{name!r}` is not the name, neither an alias of the command '
                    f'`{func!r}`.')
            
            try:
                command = commands[name]
            except KeyError:
                raise ValueError(f'At the passed name `{name!r}` there is no command removed, so it cannot be '
                    f'deleted either.')
            
            if func is not command:
                raise ValueError(f'At the specified name `{name!r}` there is a different command added already.')
            
            aliases.remove(name)
            if not aliases:
                func.aliases = None
            
            func._alters.difference_update(name_alters)
            
            for alter in name_alters:
                try:
                    del commands[alter]
                except KeyError:
                    pass
            
            return
            
        if name is None:
            raise TypeError(f'`name` should have been passed as `str`, if `func` is not passed as '
                f'`{Command.__name___}` instance, `{func!r}`.')
        
        if name == 'default_event':
            if func is self._default_event:
                self._default_event = None
                self._default_event_checks = None
                return
            
            raise ValueError(f'The passed `{name!r}` ({func!r}) is not the same as the already loaded one: '
                f'`{self._default_event!r}`')
        
        if name == 'invalid_command':
            if func is self._invalid_command:
                self._invalid_command = None
                self._invalid_command_checks = None
                return
            
            raise ValueError(f'The passed `{name!r}` ({func!r}) is not the same as the already loaded one: '
                 f'`{self._invalid_command!r}`')
        
        if name == 'command_error':
            if func is self._command_error:
                self._command_error = None
                self._command_error_checks = None
                return
            
            raise ValueError(f'The passed `{name!r}` ({func!r}) is not the same as the already loaded one: '
                f'`{self._command_error!r}`')
        
        commands = self.commands
        try:
            command = commands[name]
        except KeyError:
            raise ValueError(f'The passed `{name!r}` is not added as a command right now.') from None
        
        if not compare_converted(command.command, func):
            raise ValueError(f'The passed `{name!r}` (`{func!r}`) command is not the same as the already loaded one: '
                f'`{command!r}`')
        
        for alter in command._alters:
            try:
                del commands[alter]
            except KeyError:
                pass
        
        return
    
    async def __call__(self, client, message):
        """
        Calls the waitfors of the command processer, processes the given `message`'s content, and calls a command if
        found, or an other specified event.
        
        > Details under ``CommandProcesser``'s own docs.
        
        Arguments
        ---------
        client : ``Client``
            The client, who received the message.
        message : ``Message``
            The received message.
        
        Raises
        ------
        Any
        """
        await self.call_waitfors(client, message)
        
        if message.author.is_bot:
            return
        
        if not message.channel.cached_permissions_for(client).can_send_messages:
            return
        
        result = await self.prefixfilter(message)
        
        if result is None:
            #start goto if needed
            while self.mention_prefix:
                mentions = message.mentions
                if mentions is None:
                    break
                
                if client not in message.mentions:
                    break
                
                result = USER_MENTION_RP.match(message.content)
                if result is None or int(result.group(1)) != client.id:
                    break
                
                result = COMMAND_RP.match(message.content, result.end())
                if result is None:
                    break
                
                command_name,content=result.groups()
                command_name=command_name.lower()
                
                try:
                    command = self.commands[command_name]
                except KeyError:
                    break
                
                try:
                    result = await command(client,message,content)
                except BaseException as err:
                    command_error = self._command_error
                    if (command_error is not None):
                        checks = self._invalid_command_checks
                        if (checks is not None):
                            for check in checks:
                                if await check(client, message):
                                    continue
                                
                                handler = check.handler
                                if (handler is not None):
                                    handler(client, message, command, check)
                                break
                            else:
                                await command_error(client, message, command, content, err)
                                return
                    
                    await client.events.error(client, repr(self), err)
                    return
                
                else:
                    if result:
                        return
                
                break
        
        else:
            command_name,content=result
            command_name=command_name.lower()
            
            try:
                command=self.commands[command_name]
            except KeyError:
                invalid_command = self._invalid_command
                if (invalid_command is not None):
                    checks = self._invalid_command_checks
                    if (checks is not None):
                        for check in checks:
                            if await check(client, message):
                                continue
                            
                            handler = check.handler
                            if (handler is not None):
                                handler(client, message, command_name, check)
                            return
                    
                    await invalid_command(client,message,command_name,content)
                
                return
            
            try:
                result = await command(client, message, content)
            except BaseException as err:
                command_error = self._command_error
                if (command_error is not None):
                    checks = self._invalid_command_checks
                    if (checks is not None):
                        for check in checks:
                            if await check(client, message):
                                continue
                            
                            handler = check.handler
                            if (handler is not None):
                                handler(client, message, command, check)
                            break
                        else:
                            await command_error(client, message, command_name, content, err)
                            return
                
                await client.events.error(client, repr(self), err)
                return
            
            else:
                if result:
                    return
                
                invalid_command = self._invalid_command
                if (invalid_command is not None):
                    checks = self._invalid_command_checks
                    if (checks is not None):
                        for check in checks:
                            if await check(client, message):
                                continue
                            
                            handler = check.handler
                            if (handler is not None):
                                handler(client, message, command_name, check)
                            return
                    
                    await invalid_command(client, message, command_name, content)
                
                return
        
        default_event = self._default_event
        if (default_event is not None):
            await default_event(client, message)
        
        return
    
    def __repr__(self):
        """Returns the command processer's representation."""
        result = [
            '<', self.__class__.__name__,
            ' prefix=', repr(self.prefix),
            ', command count=', repr(self.command_count),
            ', mention_prefix=', repr(self.mention_prefix),
                ]
        
        default_event = self._default_event
        if (default_event is not None):
            result.append(', default_event=')
            result.append(repr(default_event))
            
            checks = self._default_event_checks
            if (checks is not None):
                result.append(' (with ')
                result.append(repr(len(checks)))
                result.append(')')
        
        invalid_command = self._invalid_command
        if (invalid_command is not None):
            result.append(', invalid_command=')
            result.append(repr(invalid_command))
            
            checks = self._invalid_command_checks
            if (checks is not None):
                result.append(' (with ')
                result.append(repr(len(checks)))
                result.append(')')
            
        command_error = self._command_error
        if (command_error is not None):
            result.append(', command_error=')
            result.append(repr(command_error))
            
            checks = self._command_error_checks
            if (checks is not None):
                result.append(' (with ')
                result.append(repr(len(checks)))
                result.append(')')
        
        result.append('>')
        
        return ''.join(result)
    
    @property
    def command_count(self):
        """
        Returns the amount of commands of the command processer.
        
        Returns
        -------
        command_count : `int`
        """
        count=0
        for category in self.categories:
            count+=len(category.commands)
        
        return count
    
    def _get_default_event(self):
        return self._default_event
    
    def _set_default_event(self, default_event):
        default_event = check_argcount_and_convert(default_event, 2, '`default_event` expects 2 arguments (client, '
            'message).')
        self._default_event = default_event
    
    def _del_default_event(self):
        self._default_event = None
    
    default_event = property(_get_default_event, _set_default_event, _del_default_event)
    del _get_default_event, _set_default_event, _del_default_event
    
    if (__new__.__doc__ is not None):
        default_event.__doc__ = ("""
        A get-set-del property for changing the command processer's default event.
        
        If the received message was not a comamnd call, then this event is ensured (if set) with 2 arguments:
        
        +-------------------+---------------+
        | Respective name   | Type          |
        +===================+===============+
        | client            | ``Client``    |
        +-------------------+---------------+
        | message           | ``Message``   |
        +-------------------+---------------+
        """)
    
    def _get_default_event_checks(self):
        default_event_checks = self._default_event_checks
        if (default_event_checks is not None):
            default_event_checks = default_event_checks.copy()
        
        return default_event_checks
    
    def _set_default_event_checks(self, checks):
        checks_processed = validate_checks(checks)
        self._default_event_checks = checks_processed
    
    def _del_default_event_checks(self):
        self._default_event_checks = None
    
    default_event_checks = property(_get_default_event_checks, _set_default_event_checks, _del_default_event_checks)
    del _get_default_event_checks, _set_default_event_checks, _del_default_event_checks
    
    if (__new__.__doc__ is not None):
        default_event_checks.__doc__ = ("""
        A get-set-del property for changing the command processer's default event's checks.
        """)
    
    def _get_command_error(self):
        return self._command_error
    
    def _set_command_error(self, command_error):
        command_error = check_argcount_and_convert(command_error, 4, '`invalid_command` expected 4 arguments (client, message, '
            'command, content).')
        
        self._command_error = command_error
    
    def _del_command_error(self):
        self._command_error = None
    
    command_error = property(_get_command_error, _set_command_error, _del_command_error)
    del _get_command_error, _set_command_error, _del_command_error
    
    if (__new__.__doc__ is not None):
        command_error.__doc__ = ("""
        A get-set-del property for changing the command processer's command error handler.
        
        If a command call was executed by the `commands` or by the `mention_prefix` part and the command raised, then
        `command_error` is called with the details:
        
        +-------------------+-------------------+
        | Respective name   | Type              |
        +===================+===================+
        | client            | ``Client``        |
        +-------------------+-------------------+
        | message           | ``Message``       |
        +-------------------+-------------------+
        | command           | ``Command``       |
        +-------------------+-------------------+
        | content           | `str`             |
        +-------------------+-------------------+
        | err               | ``BaseException`` |
        +-------------------+-------------------+
        """)
    
    def _get_command_error_checks(self):
        command_error_checks = self._command_error_checks
        if (command_error_checks is not None):
            command_error_checks = command_error_checks.copy()
        
        return command_error_checks
    
    def _set_command_error_checks(self, checks):
        checks_processed = validate_checks(checks)
        self._command_error_checks = checks_processed
    
    def _del_command_error_checks(self):
        self._command_error_checks = None
    
    command_error_checks = property(_get_command_error_checks, _set_command_error_checks, _del_command_error_checks)
    del _get_command_error_checks, _set_command_error_checks, _del_command_error_checks
    
    if (__new__.__doc__ is not None):
        command_error_checks.__doc__ = ("""
        A get-set-del property for changing the command processer's command error's checks.
        """)
    
    def _get_invalid_command(self):
        return self._invalid_command
    
    def _set_invalid_command(self, invalid_command):
        invalid_command = check_argcount_and_convert(invalid_command, 4, '`invalid_command` expected 4 arguments (client, message, '
            'command, content).')
        self._invalid_command = invalid_command
    
    def _del_invalid_command(self):
        self._invalid_command = None
    
    invalid_command = property(_get_invalid_command, _set_invalid_command, _del_invalid_command)
    del _get_invalid_command, _set_invalid_command, _del_invalid_command
    
    if (__new__.__doc__ is not None):
        invalid_command.__doc__ = ("""
        A get-set-del property for changing the command processer's invalid command.
        
        If `prefix` is valid, but the command not exists (or it returned `0`) will be called (if set) with `4`
        arguments:
        
        +-------------------+---------------+
        | Respective name   | Type          |
        +===================+===============+
        | client            | ``Client``    |
        +-------------------+---------------+
        | message           | ``Message``   |
        +-------------------+---------------+
        | command           | `str`         |
        +-------------------+---------------+
        | content           | `str`         |
        +-------------------+---------------+
        """)
    
    def _get_invalid_command_checks(self):
        invalid_command_checks = self._invalid_command_checks
        if (invalid_command_checks is not None):
            invalid_command_checks = invalid_command_checks.copy()
        
        return invalid_command_checks
    
    def _set_invalid_command_checks(self, checks):
        checks_processed = validate_checks(checks)
        self._invalid_command_checks = checks_processed
    
    def _del_invalid_command_checks(self):
        self._invalid_command_checks = None
    
    invalid_command_checks = property(_get_invalid_command_checks, _set_invalid_command_checks, _del_invalid_command_checks)
    del _get_invalid_command_checks, _set_invalid_command_checks, _del_invalid_command_checks
    
    if (__new__.__doc__ is not None):
        invalid_command_checks.__doc__ = ("""
        A get-set-del property for changing the command processer's invalid command's checks.
        """)

del modulize
del NEEDS_DUMMY_INIT
