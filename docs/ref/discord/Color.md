# class `Color`

A Color object represents a RGB color. Using int instead of Color is completely fine.

- source : [color.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/color.py)

- superclasses : `int`
- lenght : 24 bit

## Properties

### `as_html`

- returns : `str`
- lenght : 7

Returns the color in HTML format.

### `as_tuple`

- returns : `tuple`
- lenght : 3
- values : `int`

Returns the color's Red, Green and Blue value.

### `red`

- returns : `int`
- values : 0-255

The color's red value.

### `green`

- returns : `int`
- values : 0-255

The color's green value.

### `blue`

- returns : `int`
- values : 0-255

The color's blue value.

## Classmethods

### `from_html(cls,value)`

- returns : [`Color`](Color.md)

Converts a HTML color code to a Color object.
Raises `ValueError` on failure.

### `from_tuple(cls,value)`

- returns : [`Color`](Color.md)

Converts a tuple of ints to a Color object.
Does not checks if each element of the tuple is in 0-255, so inputting bad values can yield to bad result.

### `from_rgb(cls,r,g,b)`

- returns : [`Color`](Color.md)

Converts red, green and blue to a Color object.
Does not checks if each element of the tuple is in 0-255, so inputting bad values can yield to bad result.

## Magic methods

### `__repr__(self)`

- returns : `str`

Returns the representation of the color.
