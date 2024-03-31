# Integration

At the start of the guide we integrated the bot to a guild, but they can also be integrated with users as well.
If we go back to
[Getting Started / Inviting your bot](./getting_started.md#inviting-your-bot)
there is an extra `Try It Now` option when authorizing the bot. By selecting it, you can integrate its commands
to your user.

> Integrating is only meaningful only for global commands.

### Integration types

By defaults commands are integrated to guilds installations only.
To install commands to users as well or just to users, you have to use the `integration_types` parameter when
registering them.


```py3
@Nitori.interactions(integration_types = ['guild_install', 'user_install'], target = 'user')
async def banner(target):
    banner_url = target.banner_url_as(size = 4096)
    
    embed = Embed(f'{target.full_name}\'s banner')
    if banner_url is None:
        embed.description = 'The user has no banner'
    
    else:
        embed.url = banner_url
        embed.add_image(banner_url)
    
    return embed
```

# Integration context types

Integration contexts tell where a command can be used. The default behavior is that commands can be used anywhere.


Here is a short table for the available contexts and with which integration they are meaningful with.

| Context               | Meaningful with   |
|-----------------------|-------------------|
| `guild`               | any               |
| `bot_private_channel` | any               |
| `any_private_channel` | `user_install`    |


A common use case is to disable commands in private channels, to do that pass only `guild` as value.

```py3
@Nitori.interactions(integration_context_types = ['guild'], is_global = True)
async def guild_features(event):
    """Shows the guild's features."""
    guild = event.guild
    
    return Embed(
        f'{guild.name}\'s features',
        ', '.join(sorted(feature.name for feature in guild.iter_features())),
    ).add_thumbnail(
        guild.icon_url
    )
```

----

<p align="left">
    <a href="./slash.md">Previously: Slash & Context commands</a>
</p>

<p align="right">
    <a href="./auto_completion.md">Next up: Auto completion</a>
</p>
