# class `DiscordException`

Represents an exception raised by Discord, when it respons with a not
expected response code.

- source : [exceptions.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/exceptions.py)


###### Response codes and behaviours

| Code  | Meaning               | Behaviour     |
|-------|-----------------------|---------------|
| 200   | OK                    | return        |
| 201   | CREATED               | return        |
| 204   | NO CONTENT            | return        |
| 304   | NOT MODIFIED          | return        |
| 400   | BAD REQUEST           | raise         |
| 401   | UNAUTHORIZED          | raise         |
| 403   | FORBIDDEN             | raise         |
| 404   | NOT FOUND             | raise         |
| 405   | METHOD NOT ALLOWED    | raise         |
| 429   | TOO MANY REQUESTS     | ratelimited   |
| 500   | SERVER ERRROR         | \*retry       |
| 502   | GATEWAY UNAVAILABLE   | \*retry       |
| 5XX   | SERVER ERROR          | raise         |

> \* For five times a request can fail with `OsError` or return `501` / `502`
> response code. If the request fails with these cases for the fifth try and
> the last one resulted `501` or `502` response code, then `DiscordException`
> will be raised.

## Instance attributes

### `data`

- type : `str` / `list` / `dict` / `NoneType`

The decoded data of the respons raising this exception.

### `response`

- type : `ClientResponse`

Discord's response, what caused the expcetion.

## Properties

### `code`

- returns : `int`
- default : `0`

Returns the Discord's internal exception code, if it is included in the
response's data. If not, then returns `0`.

###  `status`

- returns : `int`

The exception's response's status.

### `messages`

- returns : `list`
- elements : `str`

Returns a list of the errors. The 0th element of the list is always a
header line, what contains the exception's name, the response's reason
and it's status. If set, then also the Discord's internal error code and
it's message as well.

Every other element at the list is optional. Those are extra extra errors
included in the reponse's data.

## Magic methods

### `__init__(self,response,data)`

Creates a [`DiscordException`](DiscordException.md).

### `__repr__`

- returns : `str`

Returns the representation of the exception. It is all the
[`._messages`](#_messages-instance-attribute) of the exception, connected with
linebreak (`\n`) together.

### `__str__`

- returns : `str`

Same as [`__repr__`](__repr__.md).

## Internal

### `_code` (instance attribute)

- type : `int` / `Nonetype`
- default : `None` / `0`

An instance attribute used for caching the Discord's internal exception code
for this error.
Initially the `._code` attribute is set to `None`, but first time when the
`.code` property is accessed, it is parsed out.
If the reponse data does not contains `code`, then this attribute is set
to `0`.

### `_cr_code` (method)

- returns : `int`
- default : `0`

Parses out the Discord's inner exception code from the response's data. Sets
it to `._code` and returns it as well.

### `_messages` (instance attribute)

- type : `list` / `NoneType`
- default : `None`
- elements : `str`

An instance attribute used for caching for the `.messages` property.
Initally the `._messages` attribute is `None`, but when the `.messages`
property is used for the first time, the messages will be parsed out
from the resposne and from it's data.

### `_cr_messages` (method)

- returns : `list`
- elements : `str`

First parses out the exception's header line from the respons. If the
response's data contains `code` or / and `message` as well, then it will
complemnet the header line with those too.

If the response's data contains additional errors too, then those will be
parsed out, and added to the list.

Saves the result to the `._messages` instance attribute and saves it as well.

