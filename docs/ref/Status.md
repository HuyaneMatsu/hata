# class `Status`

Represents a Discord [user's](User.md) status.

- Source : [others.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/others.py)

The type is used at:

| class.attribute                                   | as                                                            |
|---------------------------------------------------|---------------------------------------------------------------|
| [UserBase](UserBase.md).status                    | property                                                      |
| [Client](Client.md).status                        | instance attribute                                            |
| [User](User.md).status                            | instance attribute (/property if user caching is disabled)    |
| [UserOA2](UserOA2.md).status                      | property                                                      |
| [WebhookRepr](WebhookRepr.md).status              | property                                                      |
| [GWUserReflection](GWUserReflection.md).status    | property                                                      |

For fast status checks it is recommended to use `is`, thats why we dont just
store statuses as `str`, but as a different type. Also to avoid confusion,
`.statuses` attributes contain only `str` keys and values.
                      
## Instance attribute

| name      | type  | description                                           |
|-----------|-------|-------------------------------------------------------|
| position  | int   | A value based on the status'es color to compare them. |
| value     | str   | The status'es name.                                   |

## Class attributes

##### Predefined class attributes

There are 5 type of statuses:

| value     | position  |
|-----------|-----------|
| online    | 0         |
| idle      | 1         |
| dnd       | 2         |
| offline   | 3         |
| invisible | 3         |

### `INSTANCES`

- type : `dict`

Each status is accessable with it's [`.value`](#instance-attribute).
This is how `str` statuses are converted to [`Status`](Status.md) status.

## Properties

### `name`

- returns : `str`

Returns the status'es `value`.

## Magic methods

### `__gt__`, `__ge__`, `__eq__`, `__ne__`, `__le__`, `__lt__`

Compares the two status'es position. If the other object is `str`, then tries
to convert it to `Status` first.

### `__str__`

Returns the status'es `value`.

### `__repr__`

Returns the representation of the status.

## Internal

### `__init__(self,value,position)`

Creates a [`Status`](Status.md) with the given arguments. Adds it to it's
classe's [`.INSTANCES`](#instances).

