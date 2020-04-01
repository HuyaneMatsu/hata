# class `UserFlag`

The hypesquad flags of an account.

- Source : [user.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/user.py)

A user can be part of 9 hypesquad houses:
- [`discord_employee`](#discord_employee)
- [`discord_partner`](#discord_partner)
- [`hypesquad_events`](#hypesquad_events)
- [`bug_hunter`](#bug_hunter)
- [`hypesquad_bravery`](#hypesquad_bravery)
- [`hypesquad_brilliance`](#hypesquad_brilliance)
- [`hypesquad_balance`](#hypesquad_balance)
- [`early_supporter`](#early_supporter)
- [`team_user`](#team_user)

## Superclasses

- `int`

## Properties

### `discord_employee`

- returns : `int`
- values : `1` / `0`

Returns 1 if the flag's owner is a `discord_employee`.

### `discord_partner`

- returns : `int`
- values : `1` / `0`

Returns 1 if the flag's owner is a `discord_partner`.

### `hypesquad_events`

- returns : `int`
- values : `1` / `0`

Returns 1 if the flag's owner is `hypesquad_events` member.

### `bug_hunter`

- returns : `int`
- values : `1` / `0`

Returns 1 if the flag's owner is a `bug_hunter`.

### `hypesquad_bravery`

- returns : `int`
- values : `1` / `0`

Returns 1 if the flag's owner is `hypesquad_bravery` member.

### `hypesquad_brilliance`

- returns : `int`
- values : `1` / `0`

Returns 1 if the flag's owner is `hypesquad_brilliance` member.

### `hypesquad_balance`

- returns : `int`
- values : `1` / `0`

Returns 1 if the flag's owner is `hypesquad_balance` member.

### `early_supporter`

- returns : `int`
- values : `1` / `0`

Returns 1 if the flag's owner is an `early_supporter`.

### `team_user`

- returns : `int`
- values : `1` / `0`

Returns 1 if the flag's owner is an `team_user`.

### `system`

- returns : `int`
- values : `1` / `0`

Returns 1 if the flag's owner is a Official Discord System user (part of the
urgent message `system`).

## Magic methods

### `__iter__(self)`

- returns : `generator`
- yields : `str`

At the case of iterating a flag, it yields the flag's owner's hypesquad houses.

### `__repr__(self)`

- returns : `str`

Returns the representation of the user flag.