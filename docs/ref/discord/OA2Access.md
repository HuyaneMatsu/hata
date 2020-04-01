# class `OA2Access`

Represents a Discord oauth2 access object, what is returned by
[`Client.activate_authorization_code`](Client.md#activate_authorization_codeselfredirect_urlcodescopes)
after activating the authorization code went successfully.

- source : [oauth2.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/oauth2.py)

## Instance attribtes

### `access_token`

- type : `str`

This token is used for `Bearer` authorazitions, when requesting OAuth2 data
about the user.

### `created_at`

- type : `datetime`

The date of the activation, or of the last renewal of the access.

### `expires_in`

- type : `int`

The time in seconds, after the access expires.

Using [`.created_at`](#created_at) with [`.expires_in`](#expires_in) you can
determine, when you should renew the access.

### `redirect_url`

- type : `str`

The redirect url with what the user granted the authorization code for the
oauth2 scopes for the application.

> Can be empty string if application's onwer access was requested.

### `refresh_token`

- `str`

Token used to renew the acces token.

> Can be empty string if application's onwer access was requested.

### `scopes`

- type : `list`
- elements : `str`

A list of the scopes, what the user granted with the access token.

## Class attributes

### `TOKEN_TYPE`

- type : `str`
- values : `'Bearer'`

The `OA2Access`'s [`.access_token`](#access_token)'s type.

## Magic methods

### __repr__(self):

Returns the representation of the `OA2Access`.

## Internal

### `__init__(self,data,redirect_url)` (magic method)

Fills up the `OA2Access`'s attributes with the data sent by Discord and with
the passed `redirect_url`.

### `_renew(self,data)` (method)

Called after the oauth2 access token was renewed. If `data` is passed as
`None`, will just update [`.created_at`](#created_at). Else, it will update
the attributes of the `OA2Access` as well.
