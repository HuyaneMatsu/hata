__all__ = ('CommandProcessor', )

from scarletio import WeakReferer

from ...discord.events.handling_helpers import EventWaitforBase
from ...discord.events.handling_helpers import Router, compare_converted
from ...discord.preconverters import preconvert_bool
from ...discord.utils import USER_MENTION_RP

from .category import Category
from .command import Command
from .command_helpers import (
    COMMAND_NAME_RP, default_precheck, get_prefix_parser, test_error_handler, test_name_rule, test_precheck,
    test_unknown_command, validate_category_or_command_name
)
from .context import CommandContext
from .utils import raw_name_to_display


DEFAULT_CATEGORY_NAME = 'UNCATEGORIZED'

class CommandProcessor(EventWaitforBase):
    """
    Command processor.
    
    Attributes
    ----------
    _category_name_rule : `None`, `FunctionType`
        Function to generate category display names.
        
        A category name rule should accept the following parameters:
        
        +-------+-------------------+
        | Name  | Type              |
        +=======+===================+
        | name  | `str`             |
        +-------+-------------------+
        
        Should return the following ones:
        
        +-------+-------------------+
        | Name  | Type              |
        +=======+===================+
        | name  | `str`             |
        +-------+-------------------+
    
    _command_name_rule : `None`, `FunctionType`
        Function to generate command display names.
        
        A command name rule should accept the following parameters:
        
        +-------+-------------------+
        | Name  | Type              |
        +=======+===================+
        | name  | `str`             |
        +-------+-------------------+
        
        Should return the following ones:
        
        +-------+-------------------+
        | Name  | Type              |
        +=======+===================+
        | name  | `str`             |
        +-------+-------------------+
    
    _default_category : ``Category``
        The command processor's default category.
    
    _error_handlers : `None`, `list` of `async-function`
        Function to run when a command raises an exception.
        
        The following parameters are passed to each error handler:
        
        +-------------------+-----------------------+
        | Name              | Type                  |
        +===================+=======================+
        | command_context   | ``CommandContext``    |
        +-------------------+-----------------------+
        | exception         | `BaseException`       |
        +-------------------+-----------------------+
        
        Should return the following parameters:
        
        +-------------------+-----------+
        | Name              | Type      |
        +===================+===========+
        | handled           | `bool`    |
        +-------------------+-----------+
    
    _mention_prefix_enabled : `bool`
        Whether mentioning the client at the start of a message counts as prefix.
    
    _precheck : `FunctionType`
        A function used to detect whether a message should be handled.
        
        The following parameters are passed to it:
        
        +-----------+---------------+
        | Name      | Type          |
        +===========+===============+
        | client    | ``Client``    |
        +-----------+---------------+
        | message   | ``Message``   |
        +-----------+---------------+
        
        Should return the following parameters:
        
        +-------------------+-----------+
        | Name              | Type      |
        +===================+===========+
        | should_process    | `bool`    |
        +-------------------+-----------+
    
    _prefix_getter : `async-callable`
        
        Accepts the following parameters:
        
        +-----------+---------------+
        | Name      | Type          |
        +===========+===============+
        | message   | ``Message``   |
        +-----------+---------------+
        
        Returns the given values:
        
        +-----------+-------------------+
        | Name      | Type              |
        +===========+===================+
        | prefix    | `None`, `str`     |
        +-----------+-------------------+
    
    _prefix_ignore_case : `bool`
        Whether casing in prefix is ignored.
    
    _prefix_parser : `async-callable`
        Parses the prefix down from a message's start.
        
        Accepts the following parameters:
        
        +-----------+---------------+
        | Name      | Type          |
        +===========+===============+
        | message   | ``Message``   |
        +-----------+---------------+
        
        Returns the given values:
        
        +-----------+-------------------+
        | Name      | Type              |
        +===========+===================+
        | prefix    | `None`, `str`     |
        +-----------+-------------------+
        | end       | `int`             |
        +-----------+-------------------+
    
    _prefix_raw : `str`, `tuple` of `str`, `callable`
        Raw prefix of the command processor.
    
    _self_reference : `None`, ``WeakReferer`` to ``CommandProcessor``
        Reference to the command processor itself.
    
    _unknown_command : `None`, `FunctionType`
        Called when a command would be called, but not found.
        
        Accepts the following parameters:
        
        +---------------+---------------+
        | Name          | Type          |
        +===============+===============+
        | client        | ``Client``    |
        +---------------+---------------+
        | message       | ``Message``   |
        +---------------+---------------+
        | command_name  | `str`         |
        +---------------+---------------+
    
    category_name_to_category : `dict` of (`str`, ``Category``) items
        Category name to category relation.
    
    categories : `set` of ``Category``
        Categories registered to the command processor.
    
    command_name_to_command : `dict` of (`str`, ``Command``) items
        Command name to command relation.
    
    commands : `set` of ``Command``
        The registered commands to the command processor.
    
    Notes
    -----
    ``CommandProcessor`` supports weakreferencing.
    """
    
    __slots__ = (
        '__weakref__', '_category_name_rule', '_command_name_rule', '_default_category', '_error_handlers',
        '_mention_prefix_enabled', '_precheck', '_prefix_getter', '_prefix_ignore_case', '_prefix_parser',
        '_prefix_raw', '_self_reference', 'category_name_to_category', '_unknown_command', 'categories',
        'command_name_to_command', 'commands'
    )
    
    __event_name__ = 'message_create'
    SUPPORTED_TYPES = (Command, )
    
    def __new__(cls, prefix, *, precheck = None, mention_prefix_enabled=True, category_name_rule=None,
            command_name_rule=None, default_category_name=None, prefix_ignore_case=True):
        """
        Creates a new command processor instance.
        
        Parameters
        ----------
        prefix :  `str`, `tuple` of `str`, `callable`
            Prefix of the command processor.
            
            Can be given as a normal `callable` or as an `async-callable` as well, which should accept `1` parameter:
            
            +-------------------+---------------+
            | Name              | Type          |
            +===================+===============+
            | message           | ``Message``   |
            +-------------------+---------------+
            
            And return the following value:
            
            +-------------------+---------------------------+
            | Name              | Type                      |
            +===================+===========================+
            | prefix            | `str`, `tuple` of `str`   |
            +-------------------+---------------------------+
            
        precheck : `None`, `callable` = `None`, Optional (Keyword only)
            A function used to detect whether a message should be handled.
        mention_prefix_enabled : `bool` = `True`, Optional (Keyword only)
            Whether mentioning the client at the start of a message counts as prefix. Defaults to `True`.
        category_name_rule : `None`, `FunctionType` = `None`, Optional (Keyword only)
            Function to generate category display names. Defaults to `None`.
        command_name_rule : `None`, `FunctionType` = `None`, Optional (Keyword only)
            Function to generate command display names. Defaults to `None`.
        default_category_name : `None`, `str` = `None`, Optional (Keyword only)
            The command processor's default category's name. Defaults to `None`.
        prefix_ignore_case : `bool` = `True`
            Whether the prefix's case should be ignored.
        
        Raises
        ------
        TypeError
            - If `precheck` accepts bad amount of parameters.
            - If `precheck` is async.
            - If `mention_prefix_enabled` was not given as a `bool`.
            - If `category_name_rule` is not `None` nor `function`.
            - If `category_name_rule` is `async-function`.
            - If `category_name_rule` accepts bad amount of parameters.
            - If `category_name_rule` raises exception when `str` is passed to it.
            - If `category_name_rule` not returns `str`, when passing `str` to it.
            - If `command_name_rule` is not `None` nor `function`.
            - If `command_name_rule` is `async-function`.
            - If `command_name_rule` accepts bad amount of parameters.
            - If `command_name_rule` raises exception when `str` is passed to it.
            - If `command_name_rule` not returns `str`, when `str` is passed to it.
            - If `default_category_name` was not given neither as `None` nor as `str`.
            - If `prefix_ignore_case` was not given as `bool`.
            - Prefix's type is incorrect.
            - Prefix is a callable but accepts bad amount of parameters.
        ValueError
            - If `default_category_name`'s length is out of range [1:128].
        """
        if (category_name_rule is not None):
            test_name_rule(category_name_rule, 'category_name_rule')
        
        if (command_name_rule is not None):
            test_name_rule(command_name_rule, 'command_name_rule')
        
        if default_category_name is None:
            default_category_name = DEFAULT_CATEGORY_NAME
        else:
            default_category_name = validate_category_or_command_name(default_category_name)
        
        default_category = Category(default_category_name)
        
        if precheck is None:
            precheck = default_precheck
        else:
            test_precheck(precheck)
        
        mention_prefix_enabled = preconvert_bool(mention_prefix_enabled, 'mention_prefix_enabled')
        prefix_ignore_case = preconvert_bool(prefix_ignore_case, 'prefix_ignore_case')
        
        prefix_parser, prefix_getter = get_prefix_parser(prefix, prefix_ignore_case)
        
        self = object.__new__(cls)
        self._self_reference = None
        self._precheck = precheck
        self._error_handlers = None
        self._mention_prefix_enabled = mention_prefix_enabled
        self._category_name_rule = category_name_rule
        # Assign it later, exception may occur
        self._self_reference = WeakReferer(self)
        self._prefix_ignore_case = prefix_ignore_case
        self._prefix_parser = prefix_parser
        self._prefix_raw = prefix
        self._prefix_getter = prefix_getter
        self._default_category = default_category
        self._command_name_rule = command_name_rule
        self._category_name_rule = category_name_rule
        self.command_name_to_command = {}
        self.category_name_to_category = {}
        self.commands = set()
        self.categories = set()
        self._unknown_command = None
        
        self._self_reference = WeakReferer(self)
        
        default_category.set_command_processor(self)
        
        return self
    
    
    async def __call__(self, client, message):
        """
        Calls the waitfors of the command processor, processing the given `message`'s content, and calls a command if
        found, or an other specified event.
        
        Details under ``CommandProcessor``'s own docs.
        
        This method is a coroutine.
        
        Parameters
        ---------
        client : ``Client``
            The client, who received the message.
        message : ``Message``
            The received message.
        """
        await self.call_waitfors(client, message)
        
        if not self._precheck(client, message):
            return
        
        prefix, end = await self._prefix_parser(message)
        if (prefix is None):
            if not self._mention_prefix_enabled:
                return
            
            user_mentions = message.user_mentions
            if (user_mentions is None) or (client not in user_mentions):
                return
            
            content = message.content
            if content is None:
                return
            
            parsed = USER_MENTION_RP.match(content)
            if (parsed is None) or (int(parsed.group(1)) != client.id):
                return
            
            end = parsed.end()
        
        content = message.content
        if content is None:
            return
        
        parsed = COMMAND_NAME_RP.match(content, end)
        if (parsed is None):
            return
        
        command_name = parsed.group(1)
        end = parsed.end()
        
        command_name = raw_name_to_display(command_name)
        
        try:
            command = self.command_name_to_command[command_name]
        except KeyError:
            pass
        else:
            content = content[end:]
            
            if prefix is None:
                prefix = await self._prefix_getter(message)
            
            context = CommandContext(client, message, prefix, content, command)
            if await context.invoke():
                return
        
        
        unknown_command = self._unknown_command
        if (unknown_command is not None):
            try:
                await unknown_command(client, message, command_name)
            except GeneratorExit:
                raise
            
            except BaseException as err:
                await client.events.error(client, f'{self!r}.__call__', err)
    
    
    def error(self, error_handler):
        """
        Adds na error handler to the command processor.
        
        Parameters
        ----------
        error_handler : `async-callable`
            The error handler to add.
            
            The following parameters are passed to each error handler:
            
            +-------------------+-----------------------+
            | Name              | Type                  |
            +===================+=======================+
            | command_context   | ``CommandContext``    |
            +-------------------+-----------------------+
            | exception         | `BaseException`       |
            +-------------------+-----------------------+
            
            Should return the following parameters:
            
            +-------------------+-----------+
            | Name              | Type      |
            +===================+===========+
            | handled           | `bool`    |
            +-------------------+-----------+
        
        Returns
        -------
        error_handler : `async-callable`
        
        Raises
        ------
        TypeError
            - If `error_handler` accepts bad amount of parameters.
            - If `error_handler` is not async.
        """
        test_error_handler(error_handler)
        
        error_handlers = self._error_handlers
        if error_handlers is None:
            error_handlers = self._error_handlers = []
            
            error_handlers.append(error_handler)
        
        return error_handler
    
    
    def update_prefix(self, *, prefix = None, prefix_ignore_case=None):
        """
        Updates the prefix of he
        
        Returns
        -------
        prefix :  `str`, `tuple` of `str`, `callable`, Optional (Keyword only)
            Prefix of the command processor.
            
            Can be given as a normal `callable` or as an `async-callable` as well, which should accept `1` parameter:
            
            +-------------------+---------------+
            | Name              | Type          |
            +===================+===============+
            | message           | ``Message``   |
            +-------------------+---------------+
            
            And return the following value:
            
            +-------------------+---------------------------+
            | Name              | Type                      |
            +===================+===========================+
            | prefix            | `str`, `tuple` of `str`   |
            +-------------------+---------------------------+
        
        prefix_ignore_case : `bool`, Optional (Keyword only)
            Whether the prefix's case should be ignored.
        
        Raises
        ------
        TypeError
            - If `prefix_ignore_case` was not given as `bool`.
            - Prefix's type is incorrect.
            - Prefix is a callable but accepts bad amount of parameters.
        """
        if (prefix is None) and (prefix_ignore_case is None):
            return
        
        if prefix is None:
            prefix = self._prefix_raw
        
        if prefix_ignore_case is None:
            prefix_ignore_case = self._prefix_ignore_case
        
        prefix_ignore_case = preconvert_bool(prefix_ignore_case, 'prefix_ignore_case')
        
        prefix_parser, prefix_getter = get_prefix_parser(prefix, prefix_ignore_case)
        
        self._prefix_ignore_case = prefix_ignore_case
        self._prefix_parser = prefix_parser
        self._prefix_raw = prefix
        self._prefix_getter = prefix_getter
    
    
    async def get_prefix(self, message):
        """
        Gets prefix relating to the given message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``
            The respective message.
        
        Returns
        -------
        prefix : `None`, `str`
        """
        return await self._prefix_getter(message)
    
    
    def get_category(self, category_name):
        """
        Returns the category for the given name. If the name is passed as `None`, then will return the default category
        of the command processor.
        
        Returns `None` if there is no category with the given name.
        
        Parameters
        ---------
        category_name : `None`, `str`
            The category's name.
        
        Returns
        -------
        category : `None`, ``Category``
        
        Raises
        ------
        TypeError
            If `category_name` was not given neither as  `None`, `str`.
        """
        if category_name is None:
            return self._default_category
        
        if not isinstance(category_name, str):
            raise TypeError(
                f'`category_name` can be `None`, `str`, got {category_name.__class__.__name__}; {category_name!r}.'
            )
        
        category_name = raw_name_to_display(category_name)
        
        return self.category_name_to_category.get(category_name, None)
    
    
    def get_default_category(self):
        """
        Returns the command processor's default category.
        
        Returns
        -------
        category : ``Category``
        """
        return self._default_category
    
    
    def create_category(self, category_name, *, checks=None, description = None):
        """
        Creates a category with the given parameters.
        
        Parameters
        ----------
        name : `str`
            The name of the category.
        checks : `None`, ``CheckBase``, `list` of ``CheckBase`` = `None`, Optional (Keyword only)
            Checks to define in which circumstances a command should be called.
        description : `Any` = `None`, Optional (Keyword only)
            Optional description for the category. Defaults to `None`.
        
        Returns
        -------
        category : ``Category``
        
        Raises
        ------
        TypeError
            If `checks` was not given neither as `None`, ``CheckBase``, `list` of ``CheckBase``
            instances.
        ValueError
            If a category already exists with the given name.
        """
        category_name = validate_category_or_command_name(category_name)
        if category_name in self.category_name_to_category:
            raise ValueError(
                f'There is already a category added with that name: {category_name!r}'
            )
        
        category = Category(category_name, checks=checks, description = description)
        category.set_command_processor(self)
        
        return category
    
    
    def delete_category(self, category):
        """
        Deletes the given category form the command processor.
        
        Parameters
        ----------
        category : ``Category``, `str`
            The category or the category's name to remove.
        
        Raises
        ------
        TypeError
            If `category` was not given neither as ``Category`` nor as `str`.
        ValueError
            - Default category cannot be deleted.
            - If te given category is not the same as the owned one with it's name.
        """
        if isinstance(category, Category):
            category_name = category.name
        elif isinstance(category, str):
            category_name = validate_category_or_command_name(category)
            category = None
        else:
            raise TypeError(
                f'`category` can be `{Category.__name__}`, `str`, got {category.__class__.__name__}.'
            )
        
        try:
            owned_category = self.category_name_to_category[category_name]
        except KeyError:
            return
        
        if (category is not None) and (category is not owned_category):
            raise ValueError(
                f'The given category is not the same as the owned owned one with it\'s name: got '
                f'{category!r}; owning: {owned_category!r}.'
            )
        
        owned_category.unlink()
    
    
    def _add_command(self, command):
        """
        Adds the given command to the command processor.
        
        Parameters
        ---------
        command : ``Command``
            The command to add.
        
        Raises
        ------
        RuntimeError
            - The command is bound to an other command processor.
            - The command would only partially overwrite
        """
        command_processor = command.get_command_processor()
        if (command_processor is not None) and (command_processor is not self):
            raise RuntimeError(
                f'{Command.__name__}: {command!r} is bound to an other command processor.'
            )
        
        category = command.get_category()
        if category is None:
            # Bind the command to category.
            category_hint = command._category_hint
            if category_hint is None:
                category = self._default_category
            else:
                category = self.get_category(category_hint)
                if (category is None):
                    category = self.create_category(category_hint)
            
            command.set_category(category)
        
        self.commands.add(command)
    
    
    def _remove_command(self, command):
        """
        Removes the given command from the command processor.
        
        Parameters
        ----------
        command : ``Command``
            The command to remove.
        
        Raises
        ------
        RuntimeError
            The command is bound to an other command processor.
        """
        if __debug__:
            if not isinstance(command, Command):
                raise AssertionError(
                    f'`command` can be `{Command.__name__}`, got {command.__class__.__name__}; {command!r}.'
                )
        
        command_processor = command.get_command_processor()
        if (command_processor is not None) and (command_processor is not self):
            raise RuntimeError(
                f'{Command.__name__}: {command!r} is bound to an other command processor.'
            )
        
        command.unlink_category()
        self.commands.discard(command)
    
    
    def _add_category(self, category):
        """
        Adds the given category to the command processor.
        
        Parameters
        ----------
        category : ``Category``
            The category to add.
        
        Raises
        ------
        RuntimeError
            The category is bound to an other category processor.
        """
        command_processor = category.get_command_processor()
        if (command_processor is not None) and (command_processor is not self):
            raise RuntimeError(
                f'{Category.__name__}: {command_processor!r} is bound to an other command processor.'
            )
        
        category.set_command_processor(self)
    
    
    def _remove_category(self, category):
        """
        Removes the given category to the command processor.
        
        Parameters
        ----------
        category : ``Category``
            The category to remove.
        
        Raises
        ------
        RuntimeError
            The category is bound to an other category processor.
        """
        command_processor = category.get_command_processor()
        if (command_processor is not None) and (command_processor is not self):
            raise RuntimeError(
                f'{Category.__name__}: {command_processor!r} is bound to an other command processor.'
            )
        
        category.unlink()
    
    
    @property
    def category_name_rule(self):
        """
        Get-set-del property to modify the command processor's.
        
        A category name rule is `None` or a `FunctionType` accepting the following parameters:
        
        +-------+-------------------+
        | Name  | Type              |
        +=======+===================+
        | name  | `str`             |
        +-------+-------------------+
        
        Should return the following ones:
        
        +-------+-------------------+
        | Name  | Type              |
        +=======+===================+
        | name  | `str`             |
        +-------+-------------------+
        """
        return self._category_name_rule
    
    @category_name_rule.setter
    def category_name_rule(self, category_name_rule):
        if self._category_name_rule is category_name_rule:
            return
        
        if (category_name_rule is None):
            for category in self.category_name_to_category.values():
                category.display_name = category.name
        
        else:
            test_name_rule(category_name_rule, 'category_name_rule')
            
            for category in self.category_name_to_category.values():
                category.display_name = category_name_rule(category.name)
        
        self._category_name_rule = category_name_rule
    
    @category_name_rule.deleter
    def category_name_rule(self):
        if self._category_name_rule is None:
            return
        
        for category in self.category_name_to_category.values():
            category.display_name = category.name
        
        self._category_name_rule = None
    
    
    @property
    def command_name_rule(self):
        """
        Get-set-del property to modify the command processor's.
        
        A command name rule is `None` or a `FunctionType` accepting the following parameters:
        
        +-------+-------------------+
        | Name  | Type              |
        +=======+===================+
        | name  | `str`             |
        +-------+-------------------+
        
        Should return the following ones:
        
        +-------+-------------------+
        | Name  | Type              |
        +=======+===================+
        | name  | `str`             |
        +-------+-------------------+
        """
        return self._command_name_rule
    
    @command_name_rule.setter
    def command_name_rule(self, command_name_rule):
        if self._command_name_rule is command_name_rule:
            return
        
        if command_name_rule is None:
            for command in self.commands:
                command.display_name = command.name
        else:
            test_name_rule(command_name_rule, 'command_name_rule')
            
            for command in self.commands:
                command.display_name = command_name_rule(command.name)
        
        self._command_name_rule = command_name_rule
    
    @command_name_rule.deleter
    def command_name_rule(self):
        if self._command_name_rule is None:
            return
        
        for command in self.commands:
            command.display_name = command.name
    
    
    def precheck(self, precheck):
        """
        Changes the command processor's precheck.
        
        Parameters
        ----------
        precheck : `None`, `callable`
            Can be either `None`, `non-async` function accepting following parameters are passed to it:
            
            +-----------+---------------+
            | Name      | Type          |
            +===========+===============+
            | client    | ``Client``    |
            +-----------+---------------+
            | message   | ``Message``   |
            +-----------+---------------+
            
            Should return the following parameters:
            
            +-------------------+-----------+
            | Name              | Type      |
            +===================+===========+
            | should_process    | `bool`    |
            +-------------------+-----------+
        
        Returns
        -------
        precheck : `None`, `callable`
        """
        if precheck is None:
            precheck_to_set = default_precheck
        else:
            test_precheck(precheck)
            precheck_to_set = precheck
        
        self._precheck = precheck_to_set
        return precheck
    
    def create_event(self, command, name=None, description = None, aliases=None, category=None, checks=None,
            error_handlers=None, separator=None, assigner=None, hidden=None, hidden_if_checks_fail=None):
        """
        Adds a command to the command processor.
        
        Parameters
        ----------
        command : ``Command``, ``Router``, `None`, `async-callable`
            Async callable to add as a command.
        name : `None`, `str`, `tuple` of (`None`, `Ellipsis`, `str`) = `None`, Optional
            The name to be used instead of the passed `command`'s.
        description : `None`, `Any`, `tuple` of (`None`, `Ellipsis`, `Any`) = `None`, Optional
            Description added to the command. If no description is provided, then it will check the commands's
            `.__doc__` attribute for it. If the description is a string instance, then it will be normalized with the
            ``normalize_description`` function. If it ends up as an empty string, then `None` will be set as the
            description.
        aliases : `None`, `str`, `list` of `str`, `tuple` of (`None, `Ellipsis`, `str`, `list` of `str`) = `None`
                , Optional
            The aliases of the command.
        category : `None`, ``Category``, `str`, `tuple` of (`None`, `Ellipsis`, ``Category``, `str`) = `None`
                , Optional
            The category of the command. Can be given as the category itself, or as a category's name. If given as
            `None`, then the command will go under the command processor's default category.
        checks : `None`, ``CommandCheckWrapper``, ``CheckBase``, `list` of ``CommandCheckWrapper``, ``CheckBase`` \
                instances or `tuple` of (`None`, `Ellipsis`, ``CommandCheckWrapper``, ``CheckBase``, `list` of \
                ``CommandCheckWrapper``, ``CheckBase``) = `None`, Optional
            Checks to decide in which circumstances the command should be called.
        error_handlers : `None`, `async-callable`, `list` of `async-callable`, `tuple` of (`None`, `async-callable`, \
                `list` of `async-callable`) = `None`, Optional
            Error handlers for the command.
        separator : `None`, `str`, `tuple` (`str`, `str`) = `None`, Optional
            The parameter separator of the command's parser.
        assigner : `None`, `str` = `None`, Optional
            Parameter assigner sign of the command's parser.
        hidden : `None`, `bool`, `tuple` (`None`, `Ellipsis`, `bool`) = `None`, Optional
            Whether the command should be hidden from the help commands.
        hidden_if_checks_fail : `None`, `bool`, `tuple` (`None`, `Ellipsis`, `bool`) = `None`, Optional
            Whether the command should be hidden from the help commands if any check fails.
        
        Returns
        -------
        command : ``Command``
            The added command instance.
        """
        if isinstance(command, Command):
            pass
        elif isinstance(command, Router):
            command = command[0]
        else:
            command = Command(command, name, description, aliases, category, checks, error_handlers, separator,
                assigner, hidden, hidden_if_checks_fail)
        
        self._add_command(command)
        return command
    
    
    def create_event_from_class(self, klass):
        """
        Breaks down the given class to it's class attributes and tries to add it as a command.
    
        Parameters
        ----------
        klass : `type`
            The class, from what's attributes the command will be created.
        
        Returns
        -------
        command : ``Command``
            The added command instance.
        """
        command = Command.from_class(klass)
        if isinstance(command, Router):
            command = command[0]
        
        self._add_command(command)
        return command
    
    
    def delete_event(self, command, name=None):
        """
        Removes the specified command from the command processor.
        
        Parameters
        ----------
        command : ``Command``, ``Router``, `async-callable` or instantiable to `async-callable`
            The command to remove.
        name : `None`, `str` = `None`, Optional
            The command's name to remove.
        
        Raises
        ------
        TypeError
            If `name` was not given as `None`, `str`.
        """
        if (name is not None):
            name_type = type(name)
            if name_type is str:
                pass
            elif issubclass(name_type, str):
                name = str(name)
            else:
                raise TypeError(
                    f'`name` can be `None`, `str`, got {name_type.__name__}; {name!r}.'
                )
        
        if isinstance(command, Command):
            self._remove_command(command)
            return
        
        if isinstance(command, Router):
            for command in command:
                self._remove_command(command)
            return
        
        name = raw_name_to_display(name)
        
        try:
            command = self.command_name_to_command[name]
        except KeyError:
            return
        
        command_function = command._command_function
        if (command_function is None):
            return
        
        if not compare_converted(command_function._function, command):
            return
        
        self._remove_command(command)
    
    
    def unknown_command(self, unknown_command):
        """
        Registers a function to ba called, when no prefix is found, but no command could be detected.
        
        Parameters
        ----------
        unknown_command : `None` of `FunctionType``
            The function to call.
            
            Should the following parameters:
            
            +---------------+---------------+
            | Name          | Type          |
            +===============+===============+
            | client        | ``Client``    |
            +---------------+---------------+
            | message       | ``Message``   |
            +---------------+---------------+
            | command_name  | `str`         |
            +---------------+---------------+
        
        Returns
        -------
        unknown_command : `None` of `FunctionType``
        
        Raises
        ------
        TypeError
            - If `unknown_command` accepts bad amount of parameters.
            - If `unknown_command` is not async.
        """
        test_unknown_command(unknown_command)
        self._unknown_command = unknown_command
        return unknown_command
    
    
    def __repr__(self):
        """Returns the command processor's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' command count: ')
        repr_parts.append(str(len(self.commands)))
        
        repr_parts.append(' category count: ')
        repr_parts.append(str(len(self.categories)))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
