# class `ExtensionError`

An exception raised by the [`ExtensionLoader`](ExtensionLoader.md), if loading,
reloading or unloading an extension fails with any reason.

- Source : [extension_loader.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/extension_loader.py)

## Properties

### `message`

- returns : `str`

Returns the `ExtensionError`'s message. If it has more mesages, connects them
together.

### `messages`

- returns : `list`
- elements : `str`

Returns a `list`, what contains the messages of the exception.

## Magic methods

### `__init__(self, message)`

- returns : `None`

Creates an `ExtensionError` with a message, or with a list of messages.

### `__len__(self)`

- returns : `int`

Returns the amount of messages, what the exception contains.

### `__repr__(self)`

- returns : `str`

Returns the representation of the `ExtensionError`, what contains it's
messages.

### `__str__(self)`

- returns : `str`

Same as [`.__repr__`](#__repr__self).
