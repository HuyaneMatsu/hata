# class `VoiceRegion`

Represents Discord's voice regions.

- Source : [others.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/others.py)

Each voice region is stored in the classe's [`.INSTANCES`](#instances)
`dict` class attribute, with (`id`, [`VoiceRegion`](VoiceRegion.md))
items. But they can also be accessed as `VoiceRegion.<id>`, where every 
`'-'` is replaced with `'_'` at the `id`.

## Instance attributes

| name          | type      |
|---------------|-----------|
| custom        | bool      |
| deprecated    | bool      |
| id            | str       |
| name          | str       |
| vip           | bool      |


## Class attributes

##### Predefined class attributes

There are 22 voice regions:

| id            | name              | deprecated    | vip       | custom    |
|---------------|-------------------|---------------|-----------|-----------|
| brazil        | Brazil            | False         | False     | False     |
| dubai         | Dubai             | False         | False     | False     |
| eu-central    | Central Europe    | False         | False     | False     |
| eu-west       | Western Europe    | False         | False     | False     |
| europe        | Europe            | False         | False     | False     |
| hongkong      | Hong Kong         | False         | False     | False     |
| india         | India             | False         | False     | False     |
| japan         | Japan             | False         | False     | False     |
| russia        | Russia            | False         | False     | False     |
| singapore     | Singapore         | False         | False     | False     |
| southafrica   | South Africa      | False         | False     | False     |
| sydney        | Sydney            | False         | False     | False     |
| us_central    | US Central        | False         | False     | False     |
| us-east       | US East           | False         | False     | False     |
| us-south      | US South          | False         | False     | False     |
| us-west       | US West           | False         | False     | False     |
| amsterdam     | Amsterdam         | True          | False     | False     |
| frankfurt     | Frankfurt         | True          | False     | False     |
| london        | London            | True          | False     | False     |
| vip-us-east   | VIP US West       | False         | True      | False     |
| vip-us-west   | VIP US East       | False         | True      | False     |
| vip-amsterdam | VIP Amsterdam     | True          | True      | False     |

> Custom voice regions are created runtime and they are not added as
class attributes.

### `INSTANCES`

- type : `dict`
- items : (`id`, [`VoiceRegion`](VoiceRegion.md))

Stores the created [`VoiceRegion`](VoiceRegion.md) instances. It stores the
translations of a Discord voice region ids to their representation.

## Class methods

### `from_data(cls,data)`

- returns : [`VoiceRegion`](VoiceRegion.md)

Creates a voice region from data sent by Discord.

### `get(self,id_)`

- returns : [`VoiceRegion`](VoiceRegion.md)

Tries to find the [`VoiceRegion`](VoiceRegion.md) by it's
[`.id`](#instance-attributes), if it fails, creates a new one, with
[`.from_id`](#_from_idclsid_-class-method).

## Magic methods

### `__init__(self,name,id_,deprecated,vip)`

Creates a new [`VoiceRegion`](VoiceRegion.md) and stores it at the classe's
[`.INSTANCES`](#instances).

### `__str__(self)`

- returns : `str`

Returns the voice region's name.

### `__repr__(self)`

- returns : `str`

Returns the representation of the object.

## Internal

### `_from_id(cls,id_)` (class method)

- returns : [`VoiceRegion`](VoiceRegion.md)

Creates a voice region from the given `id` and stores it.

