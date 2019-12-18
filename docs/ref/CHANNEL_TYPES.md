# tuple `CHANNEL_TYPES`

Discord channel types are stored in a dict, where their `.type` is the key and
their type is the value itself.

- Source : [channel.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/channel.py)

Every channel type is inherited from
[`ChannelBase`](ChannelBase.md).

There are two other channel superclasses:

- [`ChannelTextBase`](ChannelTextBase.md)
- [`ChannelGuildBase`](ChannelGuildBase.md)

There are six channel types, which are the following:

- [`ChannelText`](ChannelText.md)
- [`ChannelPrivate`](ChannelPrivate.md)
- [`ChannelVoice`](ChannelVoice.md)
- [`ChannelGroup`](ChannelGroup.md)
- [`ChannelCategory`](ChannelCategory.md)
- [`ChannelStore`](ChannelStore.md)

We implement 7 channel types at the wrapper, but guild text channel and guild
news share the same class type, because their type is interchangeable.
