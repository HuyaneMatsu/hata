# class `Command`

A command object stored by [`CommandProcesser`](CommandProcesser.md) in it's
[`.commands`](CommandProcesser.md#instance-attributes) and they are stored
at [`Category`](Category.md) at it's [`.commands`](Category.md#commands)
instance attribute.

- Source : [events.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/events.py)

## Instance attributes

### `aliases`

- type : `list` of `str` / `NoneType`
- default : `None`

The aliases of the command stored at a sorted list. If it has no alises, this
attribute will be set as `None`.

### `category`

- type : [`Category`](Category.md)

The command's owner category.

### `check_failure_handler`

- type : `Any`
- `awaitable` (if not `None`)
- default : `None`

An async callable, what will be added to be called, when any of the
[`.checks`](#checks) returns a positive number. By default set as `None`.

### `checks`

- type : `list` / `NoneType`
- elements : `check._check_base` instances
- default : `None`

Checks, which run before the would be called to deside if it really should,
or we should call [`.check_failure_handler`](#check_failure_handler) if set.

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
[`._normalize_description`](#_normalize_descriptiontext-function). If it
ends up as an empty string, then `None` will be set as the description.

### `needs_content`

- type : `bool`

Whether the `content` parsed by the [`CommandProcesser`](CommandProcesser.md)
should be passed to [`.command`](#command) when calling it.

### `name`

- type : `str`

The command's name.

> Always lowercase.

## Properties

### `__doc__(self)`

- returns : `str` / `None`

If [`.description`](#description) is set as `str` instance, then returns that,
else returns `None`.

## Magic methods

### `__new__(cls, name, command, needs_content, description, aliases, category, checks_, check_failure_handler)`

- returns : [`Command`](Command.md)
- raises : `ValueError` / `TypeError`

If aliases are provided as non `None`, they will be converted to a sorted list
of lower case unique strings. If the list ends up as empty, they will be set
as `None`.

If `description` is provided as `None`, then will check the passed `command`'s
`.__doc__` for it. If `description` ends up as being provided as `str`, then it
will be nomrmalized with
[`._normalize_description`](#_normalize_descriptiontext-function).

If `checks_` are provided as an empty `iterable` or as `None`, then the
attribute will be set as `None`, else it wiill be converted to a `list` and
each element will be checked, if it is `check._check_base` instance as
expected.

If `check_failure_handler` can be `None` or an async callable, what accepts 5
arguments in this order:

| name                  | type                  |
|-----------------------|-----------------------|
| client                | [Client](Client.md)   |
| message               | [Message](Message.md) |
| command               | [Command](Command.md) |
| content               | str                   |
| fail_identificator    | int                   |

If no `check_failure_handler` is provided, then the command will use it's
category's.

### `__repr__(self)`

- returns : `str`

Returns the representation of the command object.

### `__call__(self, client, message, content)`

- awaitable
- returns : `Any`

First calls the checks of it's [`.category`](#category), then it's own
[`.checks`](#checks).

If a `check` returns:
- `-2`: goes on the next.
- `-1`: stops and returns `1`, so it will be show up, like there is no
command with that name.
- `0` or more: calls [`.check_failure_handler`](#check_failure_handler) if set
as not `None` and returns it's return. If it is set as `None`, then returns `0`.

If every check passed, then awaits [`.command`](#command) with the `content`
if [needed](#needs_content) and return's it's return.

### `call_checks(self, client, message)`

- returns : `Any`
- `awaitable`

Runs the [checks](#checks) of the [`.category`](#category) and of the
command itself too. If every passes, then returns `None`. If they do not pass,
then calls [`.check_failure_handler`](#check_failure_handler) if set and
returns it's return.

### `run_checks(self, client, message)`

- retuns : `bool`

Runs [checks](#checks) of the [`.category`](#category) and of the
command itself too. If every passes, then returns `True`.

### `run_own_checks(self, client, message)`

- retuns : `bool`

Runs only the command's own [checks](#checks) without it's category's.
If every passes, then returns `True`.

### `call_command(self, client, message, content)`

- returns : `Any`
- `awaitable`

Awaits [`.command`](#command) with the `content` if [needed](#needs_content),
then return's it's return.

### `__getattr__(self,name)`

- returns : `Any`
- raises : `AttributeError`

Gets the attribute from it's [`.command`](#command) and returns it.

### `__gt__`, `__ge__`, `__eq__`, `__ne__`, `__le__`, `__lt__`

Compares the two command's name.

## Internal

### `_normalize_description(text)` (function)

- returns : `str` / `None`

Normalizes a passed string with right stripping every line, removing every
empty line from it's start and from it's end and with dedenting it.

> If the function would return an empty string, because it ends up with
> no more lines left, then it returns `None` instead.
