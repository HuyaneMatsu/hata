# class `Category`

A category stored at
[`CommandProcesser`](CommandProcesser.md)[`.commands`](CommandProcesser.md#instance-attributes).
Categories can be used to apply checks for their commands and for using
a global check failure handler for each of them as well.

- Source : [events.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/events.py)

## Instance attributes

### `commands`

- type : `sortedlist`
- elements : [`Command`](Command.md)

A sortedlist of the commands of the category.

### `desription`

- type: `Any`
- default : `None`

Description provided for the category.

### `name`

- type : `str` / `NoneType`
- default : `None`

The name of the category.

## Properties

### `checks` (get)

- returns : `list` / `NoneType`
- elements : `checks._check_base` instances
- default : `None`

The [checks](checks.md) added to the category. These always run before the
category's commands's checks.

### `checks` (set)

- raises: `TypeError`

Sets the checks for the [`Category`](Category.md). They can be set as `None` to
remove the current ones, or can be set as any `iterable` of `checks._check_base`
instances.

### `checks` (del)

Removes the checks of teh category, by setting it to `None`.

### `check_failure_handler` (get)

- returns : `Any`
- default : `None`

Returns the failure handler of the category. If it has no handler, will
return `None`.

### `check_failure_handler` (set)

- raises `TypeError`  `ValueError`

Sets a check failure handler for the category. It can be `None` or an async
callable, what accepts 5 arguments in this order:

| name                  | type                  |
|-----------------------|-----------------------|
| client                | [Client](Client.md)   |
| message               | [Message](Message.md) |
| command               | [Command](Command.md) |
| content               | str                   |
| fail_identificator    | int                   |

By modifying the failure handler of the category, it's each commands' will be
modified too, which have the same one.

### `check_failure_handler` (del)

Sets the check failure handler of the category to `None`. If it had
previously a handler, then modifies it's commands', which had the same
handler.

## Methods

### `run_own_checks(self, client, message)`

- retuns : `bool`

Runs the category's [checks](#checks-get). If every passes, then returns
`True`.

## Magic methods

### `__gt__`, `__ge__`, `__eq__`, `__ne__`, `__le__`, `__lt__`

Compares the two category's name. If the category has name as `None`, then
it will be always on the less side.

### `__new__(cls, name, checks_ = None, check_failure_handler=None, description=None)`

- returns : [`Category`](Category.md)
- raises : `ValueError` / `TypeError`

Creates an returns a new category.

### `__repr__(self)`

- returns : `str`

Returns the representation of the category.

### `__iter__(self)`

- returns : `list_iterator`

Returns an iterator over [`.commands`](#commands).

### `__reversed__(self)`

- returns : `list_reverseiterator`

Returns a reversed iteartor over [`.commands`](#commands).

### `__len__(self)`

- returns : `int`

Returns how much commands are stored at [`.commands`](#commands).

## Internal

### `_checks`(instance attribute)

- type : `list` / `NoneType`
- elements : `checks._check_base` instances
- default : `None`

The internal slot for the [`.checks`](#checks-get) property.

### `_check_failure_handler`(instance attribute)

- type : `Any`
- default : `None`

The internal slot for the [`.check_failure_handler`](#check_failure_handler-get)
property.
