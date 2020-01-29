# class `Pagination`

A builtin option to display paginated messages, what allows moving between the
pages with arrows. This class allows modifications and closing for every user.
Also works at private channels.

- Source : [events.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/events.py)

The `Pagination` picks up on reaction additions and on reaction deletions
as well, so it requires `client.event.reaction_add` and
`client.event.reaction_delete` to implement `waitfor` protocol.

`Pagination` removes the added reactions on itself, but it can happen, that the
client has no permissions to do it (like in DMs). This is why reaction deletions
is checked too.

`Pagination` expires, and to handle this expiration, it uses 
[`Timeouter`](Timeouter.md).

If the object is created only with one page, arrows wont be added as reactions
to it. Also if the `Pagination` is sent to a [channel](CHANNEL_TYPES.md), where
the [client](Client.md) can not add reactions, it will just send the
[message](Message.md) and do nothing more.

## Creating a Pagination

### `await Pagination(client,channel,pages,timeout=240.,message=None)`

##### `client`

The [client](Client.md), who will execute the API requests.

##### `channel`

The [channel](CHANNEL_TYPES.md) where the [message](Message.md) will be sent.

##### `pages`

Should be a list like container (what implements `__getitem__` and `__len__`),
what at getting any of it's items returns an [`Embed`](Embed.md).

##### `timeout`

The timeout when the `Pagination` will expire. Whenever the pagination is used,
it's timeout will be reseted.

If a `Pagination` expires, it removes it's reactions to mark, it is no longer
usable.

##### `message`

If a [`Message`](Message.md) is passed, when creating a pagination, it will 
use that message, instead of creating a new one.


## Instance attributes

### `canceller`

- type : `function` / `NoneType`
- default : [`._canceller`](#_cancellerselfexception-function)

The function called when the `Pagination` is cancelled or when it expires.
This is a one time use method, because after the system used it, it will be
modifed to `None`, to mark the `Pagination` is already cancelled.

### `channel`

- type : [`Channel`](CHANNEL_TYPES.md)

The channel where the `Pagination` is executed.

### `client`

- type : [`Client`](Client.md)

The [`Client`](Client.md), which executes the actions on the
[`Pagination`](Pagination.md).

### `message`

- type : [`Message`](Message.md) / `NoneType`
- default : `None`

The [`Pagination`](Pagination.md)'s message.

> If exception is raised meanwhile creating [`.message`](#message-1) is set to
>`None`.

### `page`

- type : `int`
- default : `0`

The currently displayed page's index.

### `pages`

- type : `Any`

The container what stores the displayable [embeds](Embed.md).

### `task_flag`

- type : `int`

A flag to store the state of the `Pagination`.

| name                      | flag  | description                                                                           |
|---------------------------|-------|---------------------------------------------------------------------------------------|
| GUI_STATE_READY           | 0     | The Pagination does nothing an it is ready to be used.                                |
| GUI_STATE_SWITCHING_PAGE  | 1     | The Pagination is currently chaning it's page.                                        |
| GUI_STATE_CANCELLING      | 2     | The pagination is currently chaning it's page, but it was cancelled meanwhile.        |
| GUI_STATE_CANCELLED       | 3     | The pagination is, or is being cancelled right now.                                   |
| GUI_STATE_SWITCHING_CTX   | 4     | The Pagination is switching context. (Not used by the default class, btu expected.)   |

### `timeout`

- type : `int`

Stores the timeout of the [`Pagination`](Pagination.md).

### `timeouter`

- type : [`Timeouter`](Timeouter.md) / `NoneType`
- default : `None`

[`Timeouter`](Timeouter.md) executes the timing out feature on the
[`Pagination`](Pagination.md).

## Class attributes

| name      | equals to                         |
|-----------|-----------------------------------|
| LEFT2     | BUILTIN_EMOJIS['track_previous']  |
| LEFT      | BUILTIN_EMOJIS['arrow_backward']  |
| RIGHT     | BUILTIN_EMOJIS['arrow_forward']   |
| RIGHT2    | BUILTIN_EMOJIS['track_next']      |
| CANCEL    | BUILTIN_EMOJIS['x']               |
| emojis    | (LEFT2,LEFT,RIGHT,RIGHT2,CANCEL)  |

## Methods

### `cancel(self,exception=None)`

Cancels the [`Pagination`](Pagination.md) [`.timeouter`](#timeouter) and
ensures it's [`.canceller`](#canceller) with the given `exception`.

## Magic methods

### `__new__(cls,client,channel,pages,timeout=240.)`

- `awaitable`
- raises : `DiscordException`

### `__call__(self,emoji,user)`

- returns : `None`
- `awaitable`

Called, when a reaction is added on remvoved on [`.message`](#message-1).

### `__repr__(self)`

- returns : `str`

Returns the representation of the [`Pagination`](Pagination.md)

## Internal

### `_canceller(self,exception)` (function)

This function is used up at cancellation and sets the object's
[`.task_flag`](#task_flag) to `GUI_STATE_CANCELLED`.

If the `exception` argument is `None`, means that the `Pagination` was
cancelled from inside, with no errors.

If the `exception` argument is `TimeoutError` instance, means that the
`Pagination` expired by it's [`.timeouter`](#timeouter). At this case it
removes the reactions on itself.

[`Pagination`] does not excepts other cancelling cases, so at every other case,
it just cancels it's [`.timeouter`](#timeouter).
