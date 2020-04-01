# tuple `ACTIVITY_TYPES`

Discord activites are stored in a tuple, where each activity is at
it's `.type` index.

- Source : [activity.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/activity.py)

Every activity type is inherited from
[`ActivityBase`](ActivityBase.md).
There is an univerzal activity type, called
[`ActivityRich`](ActivityRich.md), but there are 6 other activities too.

- [`ActivityUnknown`](ActivityUnknown.md)
- [`ActivityGame`](ActivityGame.md)
- [`ActivityStream`](ActivityStream.md)
- [`ActivitySpotify`](ActivitySpotify.md)
- [`ActivityWatching`](ActivityWatching.md)
- [`ActivityCustom`](ActivityCustom.md)

The main difference is that these are just a restricted version of the main
[`ActivityRich`](ActivityRich.md) type.

> `ActivityUnknown` is just an internal activity, Discord does not uses it.

### `Activity`

- returns : [`Activity`](ACTIVITY_TYPES.md)

A factory function to create activity from json data sent by discord.
If the data is `None` returns [`ActivityUnknown`](ActivityUnknown.md).
If the length of the data exceeds the activty type's maximal size,
it returns [`ActivityRich`](ActivityRich.md).
