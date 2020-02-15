# class `Command`

A command object stored by [`CommandProcesser`](CommandProcesser.md) in it's
[`.commands`](CommandProcesser.md#instance-attributes).

- Source : [events.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/events.py)

## Instance attributes

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
[`._normalize_description`](#_normalize_descriptiontext-staticmethod). If it
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

### `__init__(self, name, command, needs_content, description)`

Creates a [`Command`](#command) object. If `description` is provided as `None`,
then will check the passed `command`'s `__doc__` as for it.

### `__repr__(self)`

- returns : `str`

Returns the representation of the command.

### `__call__(self, client, message, content)`

- awaitable
- returns : `Any`

Calls [`.command`](#command) with the `content` if needed. Returns the
command's return.

## Internal

### `_normalize_description(text)` (staticmethod)

- returns : `str` / `None`

Normalizes a passed string with right stripping every line, removing every
empty line from it's start and from it's end and with dedenting it.

> If the function would return an empty string, because it ends up with
> no more lines left, then it returns `None` instead.
