# class `ActivityFlag`

The flags of an activity provided by Discord. These flags supposed to
describe, what the activity's payload includes.

- Source : [activity.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/activity.py)

## Superclasses

- `int`

## Class attributes

##### Predefined class attributes

| name          | value             |
|---------------|-------------------|
| spotify       | ActivityFlag(48)  |

> If an [`ActivitySpotify`](ActivitySpotify.md)'s payload not includes `flags`,
> the `ActivityFlag.spotify` will be used as a default flag.

## Properties

### `INSTANCE`

- returns : `int`
- values : `0` / `1`

### `JOIN`

- returns : `int`
- values : `0` / `1`

### `SPECTATE`

- returns : `int`
- values : `0` / `1`

### `JOIN_REQUEST`

- returns : `int`
- values : `0` / `1`

### `SYNC`

- returns : `int`
- values : `0` / `1`

### `PLAY`

- returns : `int`
- values : `0` / `1`

## Magic methods

### `__iter__(self)`

- returns : `generator`
- yields : `str`

At the case of iterating a flag, it yields it's properties' names, which it
includes.

### `__repr__(self)`

- returns : `str`

Returns the representation of the activity flag.
