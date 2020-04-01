# class `Embed`

The `Embed` object represents Discord embedded content. There are two defined
embed classes. The other one is [`EmbedCore`](EmbedCore.md).

- Source : [embed.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/embed.py)

Embeds are easier to build with this class, and faster to serialize, because
we store the objects as raw serializable data, but it also means, other
operations might be more heavy, because we need to convert the serialized
content back.

- [Embed visualiser](https://leovoel.github.io/embed-visualizer/) - *credit to leovoel*

##### Embed Limits

| Element       | Limit     | limit of  |
|---------------|-----------|-----------|
| TOTAL         | 6000      | character |
| title         | 256       | character |
| description   | 2048      | character |
| footer        | 2048      | character |
| field         | 25        | piece     |
| field name    | 256       | character |
| field value   | 1024      | character |

#### Using local image in embed

```py
#imports
from hata.ios import ReuAsyncIO
from hata.embed import Embed

#building the embed
embed=Embed()
embed.add_image('attachment://image.png')

#sending the embed (this syntax might change later)
with (await ReuAsyncIO('some_file_path')) as file:
    await client.message_create(channel,embed=embed,file=('image.png',file))
```

This example points out some importantish parts:
    
- Pointing on attachment always starts with `'attachment://...'`.
- The image's name always need to match with the attachment's name.
- The usage of asynchronous file loader, because reading from storage
  has high latency, so it counts as blocking operation.
- We need to use a buffer type, what does not closes on `close`, but it
seeks to 0 instead (or if needed), because if a request fails, we need to
be able to resend the content again. So if the buffer is already closed, then
we should get a nice error.

## Creating an Embed

### Embed(title=None,description=None,color=None,url=None,timestamp=None,type_='rich')

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
`'link'`, `'video'`, `'gifv'`, `'image'`.

## Instance attributes

### `data`

- type : `dict`
- items : (`str`, `Any`)

The raw data of the embed. It should not be accessed directly, thats why
there are several [properties](#Properties) and [methods](#Methods) to do
operations on them.

## Properties

| name          | type                                                      | access        | default   | specific methods                                          |
|---------------|-----------------------------------------------------------|---------------|-----------|-----------------------------------------------------------|
| author        | NoneType / [Embed_author](Embed_author.md)                | get-set-del   | None      | [add_author](#add_authorselficon_urlnonenamenoneurlnone)  |
| color         | NoneType / int / [Color](Color.md)                        | get-set-del   | None      |                                                           |
| description   | NoneType / str                                            | get-set-del   | None      |                                                           |
| fields        | [_EmbedFieldsReflection](_EmbedFieldsReflection.md)       | get-set-del   |           | \* add / insert / get /set / del                          |
| footer        | NoneType / [EmbedFooter](EmbedFooter.md)                  | get-set-del   | None      | [add_footer](#add_footerselftexticon_urlnone)             |
| image         | NoneType / [EmbedImage](EmbedImage.md)                    | get-set-del   | None      | [add_image](#add_imageselfurl)                            |
| provider      | NoneType / [EmbedProvider](EmbedProvider.md)              | get-del       | None      |                                                           |
| thumbnail     | NoneType / [EmbedThumbnail](EmbedThumbnail.md)            | get-set-del   | None      | [add_thumbnail](#add_thumbnailselfurl)                    |
| timestamp     | NoneType / datetime                                       | get-set-del   | None      |                                                           |
| title         | NoneType / str                                            | get-set-del   | None      |                                                           |
| type          | NoneType / str                                            | get-set-del   | None      |                                                           |
| url           | NoneType / str                                            | get-set-del   | None      |                                                           |
| video         | NoneType / [EmbedVideo](EmbedVideo.md)                    | get-del       | None      |                                                           |

> \* `fields` has more specific methods:
> - [`add_field`](#add_fieldselfnamevalueinlinefalse)
> - [`insert_field`](#insert_fieldselfindexnamevalueinlinefalse)
> - [`get_field`](#get_fieldselfindex)
> - [`set_field`](#set_fieldselfindexfield)
> - [`del_field`](#del_fieldselfindex)
>
> An own [reflection type](_EmbedFieldsReflection.md) too, what allows
> modifying the [embeds' fields](EmbedField.md) more directly.

### `source`

- get, set, del
- returns : [`EmbedCore`](EmbedCore.md)

Allows you to clear your embed, or to modify it, with simply just copying the
other or just get the [`Embed's`](Embed.md) [`EmbedCore`](EmbedCore.md)
representation.

### `contents`

- returns : `list`
- elements : `str`

Returns the embed's contents:
- title
- description
- author.name
- footer.text
- fields[n].name
- fields[n].value

## Methods

### `add_author(self,icon_url=None,name=None,url=None)`

- returns : `self`

Adds an [embed author](EmbedAuthor.md) to the embed with the given arguments.
All of these arguments are optional and they should be `str` type.

### `add_field(self,name,value,inline=False)`

- returns : `self`

Adds an [embed field](EmbedField.md) to the embed's fields.
`name` and `value` are required arguments, which should be type `str`,
meanwhile `inline` is optional and should be `bool`.

### `insert_field(self,index,name,value,inline=False)`

- returns : `None`
- raises : `IndexError`

Familiar to [add_field](#add_fieldselfnamevalueinlinefalse), but it inserts
the field at the given `index`.

### `get_field(self,index)`

- returns : [`EmbedField`](EmbedField.md)
- raises : `IndexError`

Returns the embed's field at the given index.

### `set_field(self,index,field)`

- returns : `None`
- raises : `IndexError`

Sets the given [`EmbedField`](EmbedField.md) at the given `index`.

### `del_field(self,index)`

- returns : `None`
- raises : `IndexError`

Removes the [`field`](EmbedField.md) from the given `index`

### `add_footer(self,text,icon_url=None)`

- returns : `self`

Adds an [embed author](EmbedFooter.md) to the embed with the given arguments.
The `text` argument is required, meanwhile, the `icon_url` is optional.
Both arguments supposed to be `str` type.

### `add_image(self,url)`

- returns : `self`

Adds an [embed image](EmbedImage.md) to the embed with the given arguments.
Accepts only 1 argument, the `url` of the image, what supposed to be `str` type.

### `add_thumbnail(self,url)`

- returns : `self`
Adds an [embed thumbnail](EmbedThumbnail.md) to the embed with the given
argument, what supposed to be `str` type.

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
