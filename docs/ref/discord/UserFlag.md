# class `UserFlag`

The hypesquad flags of an account.

- Source : [user.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/user.py)

## Superclasses

- `int`

## Properties

Each user flag can be checked with a property of it's name. Every property
returns and `int`, `0` or `1`, depeding if the user has that specific flag.

- `discord_employee`
- `discord_partner`
- `hypesquad_events`
- `bug_hunter_level_1`
- `mfa_sms`
- `premium_promo_dismissed`
- `hypesquad_bravery`
- `hypesquad_brilliance`
- `hypesquad_balance`
- `early_supporter`
- `team_user`
- `system`
- `bug_hunter_level_2`
- `underage_deleted`
- `verified_bot`
- `verified_bot_developer`

## Magic methods

### `__iter__(self)`

- returns : `generator`
- yields : `str`

Yields the names of the flags, what the user has.

### `__repr__(self)`

- returns : `str`

Returns the representation of the user flag.