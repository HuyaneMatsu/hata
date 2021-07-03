# Emoji

## Introduction

Hata's emoji handling might be esoteric at the first look but it is actually based on a pretty smart concept.
(I am happy about it, so it should not be that bad... right?)

Luckily Hata has only 1 emoji type; `Emoji` (we don't use emotes here), which covers custom and unicode / builtin
emojis as well.

Similarly to many Hata Discord entities, each emoji is also globally cached, preventing creating of duplicates.
This is an essential feature of Hata and many other behaviour mentioned later will be based on it.

## Builtin / unicode emojis

Unicode emojis are not special enough cases to break the rules, so they are built into Emojis. But how much
they can fit into them? - o-ho-ho perfectly! Might sound shocking but all the above mentioned rules are true for them.

Unicode emojis may be just some strings for a lot of libraries but inside the Hata they get their own name and static
identifier as well. Their identifier is hardcoded and won't change between startups, allowing developers to store
unicode emojis on the same way as static - just by storing their identifier.

Unicode emojis can either be accessed from the global `EMOJIS` cache by their `.id` as they key, by using the
`UNICODE_EMOJIS` with their name (or alternative name) or from the `UNICODE_TO_EMOJI` by their unicode value.

New unicode emoji releases won't affect Discord nor Hata, as older emojis will still be usable,
and the new releases will get their new object keeping old data unaffected.

You can access older Variant selector-16 emojis from `UNICODE_EMOJIS` as well, by using an `_vs16` postfix after their
name.

## Custom emojis

Custom emojis cannot be accessed initially before startup, since they are not yet received from Discord.
Tho in runtime, you can find them by using `EMOJIS` weak value dictionary or in their respective guild's `.emojis` dictionary as well!

It would be really really, making your imouto cry, sad if we couldn't create custom emojis before starting up.
So to keep the lolis safe, we can precreate them and they will get  updated with their actual values when we receieve data
from Discord. To do this we got `Emoji.precreate` with the following parameters:

| Parameter name    | Type      | Required  |
|-------------------|-----------|-----------|
| id                | int       | yes       |
| name              | str       | no        |
| animated          | bool      | no        |

As mentioned, only the `id` parameter is required, although if you want to call other emoji methods or properties before
runtime you should make sure that you also pass the rest as well.

## Methods & Properties

There are only 3 commonly used emoji properties and only 2 additional methods that you should memorize.

- `created_at` (property)
    
    Returns when the emoji is created.
    
    > Has format code shortcut: `c`

- `as_emoji` (property)
    
    Returns the emoji's emoji form. Should be used when sending an emoji within a message.
    
    > Has format code shortcut: `e`

- `url` (property)
    
    Returns the emoji's image url. If the emoji is unicode emoji then it returns `None` instead.

- `is_custom_emoji` (method)

    Returns whether the emoji is custom emoji.

- `is_unicode_emoji` (method)

    Returns whether the emoji is unicode emoji.

## Parsing emojis

Hata has a generic emoji parsing function called `parse_emoji` which tries to convert the passed text to a unicode
or custom emoji. On failure returns `None`.

There is also a multi-emoji parsing function, called `parse_custom_emojis`, which only parses custom emojis.

> Hata extensions may have their own emoji parsers.
