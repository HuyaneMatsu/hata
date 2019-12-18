# def `parse_emoji`

Tries to parse out an [emoji](Emoji.md) from the inputted text. This emoji
can be custom and unicode emoji as well.

If the parsing yields a custom emoji what is not loaded, the function will
return an `untrusted` partial emoji, what means it wont be stored at `EMOJIS`.

If the parsing fails the function returns `None`.

- Source : [emoji.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/emoji.py)

## parse_emoji(text) (function)

- returns : [`Emoji`](Emoji.md) / `None`
- default : `None`
