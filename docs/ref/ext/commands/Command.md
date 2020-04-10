# class `Command`

A command object stored by [`CommandProcesser`](CommandProcesser.md) in it's
[`.commands`](CommandProcesser.md#instance-attributes) and they are stored
at [`Category`](Category.md) at it's [`.commands`](Category.md#commands)
instance attribute.

- Source : [command.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/ext/commands/command.py)

## Instance attributes

### `aliases`

- type : `list` of `str` / `NoneType`
- default : `None`

The aliases of the command stored at a sorted list. If it has no alises, this
attribute will be set as `None`.

### `category`

- type : [`Category`](Category.md)

The command's owner category.

### `command`

- type : `Any`
- `awaitable`

An async callabe added as the command itself.

### `description`

- type : `Any`
- default : `None`

A description added to the command. If no description is provided, then it
will check the commands's `.__doc__` attribute.

If the description is a string instance, then it will be normalized with the
[`normalize_description`](normalize_description.md). If it
ends up as an empty string, then `None` will be set as the description.

### `name`

- type : `str`

The command's name.

> Always lowercase.

## Properties

### `check_failure_handler` (get)

- returns: `Any`
- `awaitable` (if not `None`)
- default : `None`

An async callable, what will be added to be called, when any of the
[`.checks`](#checks-get) returns a positive number. By default set as `None`.

### `check_failure_handler` (set)

- raises : `TypeError` / `ValueError`

`check_failure_handler` can be set as `None` or an async callable, what
accepts 5 arguments in this order:

| name                  | type                                  |
|-----------------------|---------------------------------------|
| client                | [Client](../../discord/Client.md)     |
| message               | [Message](../../discord/Message.md)   |
| command               | [Command](Command.md)                 |
| content               | str                                   |
| fail_identificator    | int                                   |

### `check_failure_handler` (del)

Removes the command's check failure handler by setting is as `None`.

### `checks` (get)

- returns : `list` / `NoneType`
- elements : `check._check_base` instances
- default : `None`

Returns the checks of the command. These not include the checks of the
command's category.

### `checks` (set)

Sets the checks of the command. If they are provided as an empty `iterable` or
as `None`, then the attribute will be set as `None`, else the iterable will be
converted to a `list` and each of it's elements will be checked, whether they
are `check._check_base` instances.

### `checks` (del)

Removes the command's checks, by setting them as `None`.

### `parser_failure_handler` (get)

- returns: `Any`
- `awaitable` (if not `None`)
- default : `None`

An async callable, what is called, when [`._parser`](#_parser-instance-attribute)
fails to parse every argument. By default set as `None`.

### `parser_failure_handler` (set)

- raises : `TypeError` / `ValueError`

`parser_failure_handler` can be set as `None` or an async callable, what
accepts 5 arguments in this order:

| name                  | type                                  |
|-----------------------|---------------------------------------|
| client                | [Client](../../discord/Client.md)     |
| message               | [Message](../../discord/Message.md)   |
| command               | [Command](Command.md)                 |
| content               | str                                   |
| args                  | list of Any                           |

### `parse_failure_handler` (del)

Removes the command's parser failure handler by setting is as `None`.

### `__doc__(self)`

- returns : `str` / `None`

If [`.description`](#description) is set as `str` instance, then returns that,
else returns `None`.

## Methods


### `call_checks(self, client, message)`

- returns : `Any`
- `awaitable`

Runs the [checks](#checks-get) of the [`.category`](#category) and of the
command itself too. If every passes, then returns `None`. If they do not pass,
then calls [`.check_failure_handler`](#check_failure_handler-get) if set and
returns it's return.

### `run_all_checks(self, client, message)`

- retuns : `bool`

Runs [checks](#checks-get) of the [`.category`](#category) and of the
command itself too. If every passes, then returns `True`.

### `run_checks(self, client, message)`

- retuns : `bool`

Runs only the command's own [checks](#checks-get) without it's category's.
If every passes, then returns `True`.

### `call_command(self, client, message, content)`

- returns : `Any`
- `awaitable`

Awaits [`.command`](#command) with the `content` if needed or uses
[`._parser`](#_parser-instance-attribute) and
[`.parser_failure_handler-gt`](#parser_failure_handler-get) if needed.

## Class methods

### `from_class(cls, klass, kwargs=None)`

- returns : `Command`
- raises : `TypeError` / `ValueError`

The method used, when creating a `Command` object from a class.

> Extra `kwargs` are supported as well for the usecase.

### `from_kwargs(cls, command, name, kwargs)`

- returns : `Command`
- raises : `TypeError` / `ValueError`

The method called, when a `Command` is created before adding it to a
[`CommandProceser`](CommandProcesser.md). 

## Magic methods

### `__new__(cls, command, name, needs_content, description, aliases, category, checks_, check_failure_handler)`

- returns : [`Command`](Command.md)
- raises : `ValueError` / `TypeError`

If aliases are provided as non `None`, they will be converted to a sorted list
of lower case unique strings. If the list ends up as empty, they will be set
as `None`.

If `description` is provided as `None`, then will check the passed `command`'s
`.__doc__` for it. If `description` ends up as being provided as `str`, then it
will be nomrmalized with
[`normalize_description`](normalize_description.md).

If `checks_` are provided as an empty `iterable` or as `None`, then the
attribute will be set as `None`, else it will be converted to a `list` and
each of the iterable's element will be checked, whether they are
`check._check_base` instances.

`check_failure_handler` can be `None` or an async callable, what accepts 5
arguments in this order:

| name                  | type                                  |
|-----------------------|---------------------------------------|
| client                | [Client](../../discord/Client.md)     |
| message               | [Message](../../discord/Message.md)   |
| command               | [Command](Command.md)                 |
| content               | str                                   |
| fail_identificator    | int                                   |

If no `check_failure_handler` is provided, then the command will use it's
category's.

### `__repr__(self)`

- returns : `str`

Returns the representation of the command object.

### `__call__(self, client, message, content)`

- awaitable
- returns : `Any`

First calls the checks of it's [`.category`](#category), then it's own
[`.checks`](#checks-get).

If a `check` returns:
- `-2`: goes on the next.
- `-1`: stops and returns `1`, so it will be show up, like there is no
command with that name.
- `0` or more: calls [`.check_failure_handler`](#check_failure_handler-get)
if set as not `None` and returns it's return. If it is set as `None`, then
returns `0`.

If every check passed, then checks [`._call_setting`](#_call_setting-instance-attribute)
whether it should pass `content` to [`.command`](#command) or not, or whether
it should use [`._parser`](#_parser-instance-attribute) to parse the 
message's content for specific arguments.

If the parser fails and [.parser_failure_hanler](#parser_failure_handler-get)
is not `None`, then it is ensured.

### `__getattr__(self,name)`

- returns : `Any`
- raises : `AttributeError`

Gets the attribute from it's [`.command`](#command) and returns it.

### `__gt__`, `__ge__`, `__eq__`, `__ne__`, `__le__`, `__lt__`

Compares the two command's name.

## Internal

### `_call_setting` (instance attribute)

- type : `int`

An `int` flag defines, how the command should be called. With 2 arguments,
with 3, or should we use parser.

### `_check_failure_handler` (instance attribute)

- type : `Any`
- `awaitable` (if not `None`)
- default : `None`

The internal slot used by the
[`check_failure_handler`](#check_failure_handler-get) property.

### `_checks` (instance attribute)

- type : `list` / `NoneType`
- elements : `check._check_base` instances
- default : `None`

The internal slot used by the [`checks`](#checks-get) property.

### `_parser` (instance attribute)

- type : `NoneType` / `function`
- `awaitable` (if not `None`)
- default : `None`

The generated parser function for parsing arguments if needed.

### `_parser_failure_handler` (instance attribute)

- type : `Any`
- `awaitable` (if not `None`)
- default : `None`
The internal slot used by the
[`parser_failure_handler`](#parser_failure_handler-get) property.
