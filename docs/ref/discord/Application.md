# class `Application`

Represents a Discord application with all of it's spice.

- Source : [application.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/application.py)

When a [client](Client.md) is created, it starts it's life with an empty
application by defualt. This application can be update by awaiting
`Client.update_application_info()` anytime.

## Instance attributes

| name                      | type                                                      | default   |
|---------------------------|-----------------------------------------------------------|-----------|
| bot_public                | bool                                                      | False     |
| bot_require_code_grant    | bool                                                      | False     |
| cover                     | int                                                       | 0         |
| description               | str                                                       | ''        |
| guild                     | [Guild](Guild.md) / NoneType                              | None      |
| icon                      | int                                                       | 0         |
| id                        | int                                                       | 0         |
| name                      | str                                                       | ''        |
| owner                     | [User](User.md) / [Client](Client.md) / [Team](Team.md)   | ZEROUSER  |
| primary_sku_id            | int                                                       | 0         |
| rpc_origins               | list of str                                               | []        |
| slug                      | str or NoneType                                           | None      |
| summary                   | str                                                       | ''        |
| verify_key                | str                                                       | ''        |

## Properties

### `created_at`

- returns : `datetime`

The creation time of the application.

### `cover_url`

- returns : `str` / `None`
- default : `None`

The application's cover's url. If the application has no cover, then returns
`None`.

### `icon_url`

- returns : `str` / `None`
- default : `None`

The application's icon's url. If the application has no icon, then returns
`None`.

## Methods

### `cover_url_as(self,ext=None,size=None)`

- returns : `str` / `None`
- default : `None`
- raises : `ValueError`

Returns the application's cover's url.
If the application has no cover, then returns `None`

Valid extensions: 'jpg', 'jpeg', 'png', 'webp'.
Valid sizes: 16, 32, 64, 128, 256, 512, 1024, 2048, 4096.

### `icon_url_as(self,ext=None,size=None)`

- returns : `str` / `None`
- default : `None`
- raises : `ValueError`

Returns the application's icon's url.
If the application has no icon, then returns `None`

Valid extensions: 'jpg', 'jpeg', 'png', 'webp'.
Valid sizes: 16, 32, 64, 128, 256, 512, 1024, 2048, 4096.

## Internal

### `__init__(self,data=None)` (Magic Method)

Creates an [`Application`](Application.md). If `data` is `None`, it fills up
the application's attributes with their default value, else it updates itself
with the given data.

### `_fillup(self)` (Method)

- returns : `None`

Fills up the application's instance attributes with it their default values.
Called after creating an application without any data.

### `__call__(self,data)` (Magic method)

- returns : `None`

Called to update the application with the given data.
