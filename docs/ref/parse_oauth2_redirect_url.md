# def `parse_oauth2_redirect_url`

Parses the `redirect_url` and the `code` out the whole `url`, that the user
was redircted to after outh2 authorization.

- Source : [oauth2.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/oauth2.py)

## `cr_p_overwrite_object(url)` (function)

- returns : `None` / `tuple` (`str`, `str`)

If the parsing was successful, then returns a `tuple` of `redirect_url` and
`code`. If it fails, returns `None`.

##### `url`

- type : `str`

The whole url to parse from.
