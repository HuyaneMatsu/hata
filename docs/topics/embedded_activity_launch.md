# Introduction

Launching embedded activities is done through application commands. If you are not planning to use embedded activities
in your application, you probably don't need to continue reading this topic.

If you are still here you already may have enabled embedded activities in your application in the Discord developer
portal or are just curious about the secrets this feature contains.

> Each example here showcases a different idea. Please make sure to not skip any if you decide to read the topic.

## Default entry point

By enabling embedded activities in the developer portal, Discord creates an application command for you to launch.
The default entry point is completely handled by Discord, so normally you would not need to do anything at this point,
but since Hata syncs your registered application commands with Discord, it sees that as an extra unused command that
showed up and gets rid of it.

Do not fret, the solution is simple, we just have to make an equivalent command on our side.
Similar to context commands, we use the `target` parameter to tell where it should show up.
In this particular case we pass it as: `'embedded activity launch'` (there are other non-string versions of it as well).

```py
launch = Sakuya.interactions(
    None,
    name = 'launch',
    target_type = 'embedded activity launch',
)
```

Notice how here we pass the `function` parameter as `None`.
By doing this we delegate the responsibility back to Discord to handle the interaction.

> Embedded activity launch commands can only be global, so it is not required to pass `is_global = True`.
> Defining them as not-global or guild-bound will raise an exception.
>
> Embedded activity launch commands cannot have sub-commands.

## Custom entry point

In case you don't want to send any message, send custom message(s), don't want to start the activity or just want to
execute some code, this is what you are looking for!

### No message

To just launch an embedded activity without sending any message, register a command with a bare `return`.

```py
@Sakuya.interactions(target_type = 'embedded activity launch')
async def launch():
    return
```

### Sending single message

To send a single message just return what you want to send. Embeds, attachments and polls, say no more; it's supported.

```py
@Sakuya.interactions(target_type = 'embedded activity launch')
async def launch():
    return 'Great success!'
```

An embedded activity launch command can define only the default `client` and `event` parameters.

```py
@Sakuya.interactions(target_type = 'embedded activity launch')
async def launch(client, event):
    return f'{event.user.name_at(event.guild)} launches {client.name_at(event.guild)}\'s embedded activity :3'
```

### Launching and then responding

To launch an embedded activity similar to `return`, using a `yield` also works.

```py
@Sakuya.interactions(target_type = 'embedded activity launch')
async def launch():
    yield
```

After that every additional `yield <value>` will send an additional message.

```py
@Sakuya.interactions(target_type = 'embedded activity launch')
async def launch():
    yield
    yield 'Great success!'
    yield 'More!!'
```

> Embedded activity launching uses the same underlying endpoint as acknowledgement,
> so it must be done first and within the first `3` seconds.

### Not launching

You may decide to not launch up the embedded activity. The `abort` function is your friend in every mischief.

```py
@Sakuya.interactions(target_type = 'embedded activity launch')
async def launch(client, event):
    if not client.is_owner(event.user):
        abort('Owner only!')
```

### Manual responding

In some cases the code can become complex and using either `return` / `yield` / `abort` is just not enough.
For these cases use the client methods directly.

**Example: launch activity with message**

```py
@Sakuya.interactions(target_type = 'embedded activity launch')
async def launch():
    return 'Great success!'
```

Is equivalent to:
```py
@Sakuya.interactions(target_type = 'embedded activity launch')
async def launch(client, event):
    await client.interaction_embedded_activity_launch(event)
    await client.interaction_followup_message_create(event, 'Great success!')
```
It is not possible to launch up the embedded activity and create a message with the same endpoint.
Although you can achieve this behavior by chaining `interaction_embedded_activity_launch` into a
`interaction_followup_message_create` call.

**Example: launch activity & send 2 message**

```py
@Sakuya.interactions(target_type = 'embedded activity launch')
async def launch():
    yield
    yield 'Great success!'
    yield 'More!!'
```

Is equivalent to:
```py
@Sakuya.interactions(target_type = 'embedded activity launch')
async def launch(client, event):
    await client.interaction_embedded_activity_launch(event, wait = False)
    await client.interaction_followup_message_create(event, 'Great success!')
    await client.interaction_followup_message_create(event, 'Great More!!')
```

In `interaction_embedded_activity_launch` the same `wait = False` parameter is available to run the acknowledgement
asynchronously.

**Example: Abort interaction if not owner**

```py
@Sakuya.interactions(target_type = 'embedded activity launch')
async def launch(client, event):
    if not client.is_owner(event.user):
        abort('Owner only!')
```

Is equivalent to:
```py
@Sakuya.interactions(target_type = 'embedded activity launch')
async def launch(client, event):
    if not client.is_owner(event.user):
        await client.interaction_response_message_create(event, 'Owner only!', show_for_invoking_user_only = True)
        return
    
    await client.interaction_embedded_activity_launch(event)
```

If you do not wish to launch the embedded activity you can decide to use the `interaction_response_message_create`
method instead. Or you can use `interaction_application_command_acknowledge` chained into a
`interaction_response_message_edit` call accordingly.

----

<p align="left">
    <a href="./forms.md">Previously: Forms</a>
</p>

<p align="right">
    <a href="./typing_interactions.md">Next up: Typing interactions</a>
</p>
