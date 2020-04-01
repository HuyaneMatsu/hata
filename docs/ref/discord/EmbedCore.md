# class `EmbedCore`

The `EmbedCore` object represents Discord embedded content. There are two defined
embed classes. The other one is [`Embed`](Embed.md).

- Source : [embed.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/embed.py)

Each embed what is recevied from Discord is stored as `EmbedCore`. The reason
why, because operations on this type are faster than on the other one. This
embed type is a valid embed type to send, but it is more cumbersome to build up,
because it requires extra imports and it is slow to serialize.

## Creating an Embed

### EmbedCore(title=None,description=None,color=None,url=None,timestamp=None,type_='rich')

##### `title`

The title of the embed. It shows upon at the top with intense white characters.

##### `description`

The main content of the embed.

##### `color`

The color of the embed's side. Passing `0` means black, not like at other
palces. Accepts normal `int`, and [`Color`](Color.md) too.

##### `url`

If url is passed, then the `title` will show up as a hyper link
pointing on the `url`.

##### `timestamp`

Shows up next to the footer separated with a `|`.

##### `type_`

Embed type can be `None` by default. Webhook's embeds' type must be `'rich'`.
Additional embeds under messages showing a link's content supposed to by type
`'link'`, `'video'`, `'gifv'` or `'image'`.

## Instance attributes

| name          | type                                              | default   |
|---------------|---------------------------------------------------|-----------|
| author        | NoneType / [Embed_author](EmbedAuthor.md)         | None      |
| color         | NoneType / int / [Color](Color.md)                | None      |
| description   | str                                               | None      |
| fields        | list                                              | []        |
| footer        | NoneType / [EmbedFooter](EmbedFooter.md)          | None      |
| image         | NoneType / [EmbedImage](EmbedImage.md)            | None      |
| provider      | NoneType / [EmbedProvider](EmbedProvider.md)      | None      |
| thumbnail     | NoneType / [EmbedThumbnail](EmbedThumbnail.md)    | None      |
| timestamp     | NoneType / datetime                               | None      |
| title         | str                                               | None      |
| type          | str                                               | None      |
| url           | str                                               | None      |
| video         | NoneType / [EmbedVideo](EmbedVideo.md)            | None      |

### `contents`

- returns : `list`
- elements : `str`

Returns the embed's contents, if they are set:
- title
- description
- author.name
- footer.text
- fields\[n\].name
- fields\[n\].value

## Methods

### `to_data(self)`

returns : `dict`
items : (`str` : `Any`)

Converts the [`EmbedCore`](EmbedCore.md) to json serializable dict.

## Class methods

### `from_data(cls,data)`

- returns : [`EmbedCore`](EmbedCore.md)

Creates and `EmbedCore` from data sent by Discord.

## Magic methods

### `__len__(self)`

- returns : `int`

Returns the embed's [contents'](#contents) total length.

### `__repr__(self)`

- returns : `str`

Returns the embed's representation.

### `__eq__`

- returns : `bool`

Compares the two embed.

## Internal

### `_update_sizes(self,data)` (method)

- returns : `int`
- values : `0` / `1`
- default : `0`

Called when a [`message`](Message.md) is edited, but no `edited` timestamp is
incuded with the data. Returns `0` if received data does not contains images,
at the other case `1`.

This method tries to update the embed's `image`, `thumbnail` amd `video` with
their sizes. If any of those is not set already (for any reason), then we also
create them.

### `_update_sizes_no_return(self,data)` (method)

- returns : `None`

Familiar to [`.update_sizes`](#_update_sizesselfdata-method), but returns
`None`.

### `_clean_copy(self,message)` (method)

- returns : [`EmbedCore`](EmbedCore.md)

Called by a[`Message.clean_embeds`](Message.md#clean_embeds). Copies the source
embed, except of it's `description` and each [`EmbedField`](EmbedField.md),
because it `cleans` them. Cleaning means it converts each mention to their
display text form.

