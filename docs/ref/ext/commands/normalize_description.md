# def `normalize_description`

Normalizes a passed string with right stripping every line, with
removing every empty line from it's start and from it's end, and with
dedenting.

- Source : [command.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/ext/commands/command.py)

## `normalize_description(text)` (function)

- returns : `str` / `None`

> If the function would return an empty string, because it ends up with
> no more lines left, then it returns `None` instead.