# class `MessageFlag`

The flags of a [message](Message.md).

- Source : [others.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/others.py)

A message can have 3 type of flags:
- [`crossposted`](#crossposted)
- [`is_crosspost`](#is_crosspost)
- [`embeds_suppressed`](#embeds_suppressed)

## Superclasses

- `int`

## Properties

### `crossposted`

- returns : `int`
- values : `1` / `0`

Returns 1 if the flag's [message](Message.md) is crossposted.

### `is_crosspost`

- returns : `int`
- values : `1` / `0`

Returns 1 if the flag's [message](Message.md) is a crosspost.

### `embeds_suppressed`

- returns : `int`
- values : `1` / `0`

Returns 1 if the flag's [message](Message.md) has [embeds](Message.md#embeds)
are suppressed.

### `source_message_deleted`

- returns : `int`
- values : `1` / `0`

Returns 1 if the flag's [message](Message.md)'s source message is deleted.

### `urgent`

- returns : `int`
- values : `1` / `0`

Returns 1 if the flag's [message](Message.md) came from the urgent message
system.

## Magic methods

### `__iter__(self)`

- returns : `generator`
- yields : `str`

At the case of iterating a flag, it yields the flag's [message's](Message.md)
flag's names.

### `__repr__(self)`

- returns : `str`

Returns the representation of the message flag.
