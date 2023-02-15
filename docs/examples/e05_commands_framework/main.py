from hata import Client, BUILTIN_EMOJIS, DiscordException

from hata.ext.commands_v2 import checks, CommandCheckError, CommandParameterParsingError
from hata.ext.commands_v2.helps.subterranean import SubterraneanHelpCommand

TOKEN = ''

# To setup an extension for the client, just pass its name to the `Client` constructor.
#
# Each extension has required and optional parameters. Do not forget to pass sufficient parameters for your needs.
Sakuya = Client(TOKEN,
    extensions = 'commands_v2',
    prefix = '!',
)


@Sakuya.events
async def ready(client):
    print(f'{client:f} is connected!')


# If the client is using the commands extension, you can register commands to it by using the `.commands` decorator.
@Sakuya.commands
async def about():
    """About me."""
    return 'This is a small test-bot! : )'

# The above about command will be triggered when someone sends '!about' in the chat (prefix ! is because we used that
# when we constructed the client above).


# Command context will be passed to the command if you:
# - annotated one of the arguments (either positional or keyword) as context
# - defined one of the arguments (either positional or keyword) with the name: 'ctx', 'context' or 'command_context'
# To get more information read commands topic
@Sakuya.commands
async def latency(ctx):
    """Returns my gateway latency."""
    return f'{ctx.client.gateway.latency * 1000.:.0f} ms'


# If the last parameter is positional and not annotated, the messages unused content will be passed to it.
@Sakuya.commands
async def say(ctx, content):
    """Repeats what the user passes as parameter. Ensures that users and roles are not pinged."""
    await ctx.send(content, allowed_mentions = None)


# The command processor can be accessed with the `.command_processor` attribute
#
# Error handlers to all the commands can be registered with the `.command_processor.error` decorator.
# If an error handler returns `True` no other error handlers will be called.
@Sakuya.command_processor.error
async def handle_owner_only_error(ctx, exception):
    if isinstance(exception, CommandCheckError) and (type(exception.check) is checks.CheckIsOwner):
        await ctx.send('Lacked owner permission')
        return True
    
    return False


# Annotated parameters are parsed if there is a converter for the type.
#
# You can send response message by returning or yielding any value from a command.
@Sakuya.commands
async def about_role(role: 'Role'):
    """Sends the passed role's id to the context channel."""
    return role.id
    # Here you could have also used 'yield role.id' or manually sending the message using .send method


@Sakuya.commands
async def about_channel(channel: 'Channel'):
    """Sends the passed channel's id to the context channel."""
    yield channel.id


# Command specific error handlers can be defined by `command.error` decorator.
@about_role.error
@about_channel.error
async def about_role_error_handler(ctx, exception):
    if isinstance(exception, CommandParameterParsingError):
        await ctx.send(f'{exception.content_parser_parameter.name!r} parameter is required.')
        return True
    
    return False


# We can set specific command name aside from the default function name (we can also pass list/tuples for aliases).
# Here this function will be called with '!* int int'
@Sakuya.commands(aliases='*')
async def multiply(first:int, second:int):
    """Multiplies the two numbers."""
    return first * second


# Limit commands usage to owner only.
@Sakuya.commands
@checks.owner_only()
async def ping():
    """Pongs."""
    return 'pong'


# You can get unicode (builtin) emojis by name by using the `BUILTIN_EMOJIS` dictionary.
EMOJI_CAT = BUILTIN_EMOJIS['cat']


# Limit the command to administrators only
@Sakuya.commands(aliases=['kitty', 'neko'])
@checks.has_permissions(administrator = True)
async def cat():
    """Returns a cat back."""
    return EMOJI_CAT.as_emoji


EMOJI_BIRD = BUILTIN_EMOJIS['bird']


@Sakuya.commands
async def bird(animal:str = None):
    """Bird finds animals."""
    if animal is None:
        content = f'{EMOJI_BIRD} finds animals for you.'
    else:
        content = f'{EMOJI_BIRD} could not find animal named: `{animal}`.'
    
    return content


# Example for explicit permission check.
# We could have used `@checks.has_permissions(administrator = True)` here but that would not reply by default
# (would have to define error handler and reply there).
@Sakuya.commands
async def am_i_admin(ctx):
    """Are you admin?"""
    if ctx.channel.permissions_for(ctx.author).can_administrator:
        content = 'Yes, you are.'
    else:
        content = 'No, you aren\'t.'
    
    return content


@Sakuya.commands(aliases='slow_mode')
async def slowmode(ctx, slowmode_rate: int = None):
    """Returns or sets channel slowmode."""
    if slowmode_rate is None:
        return f'The channel\'s current slowmode is: `{ctx.channel.slowmode}` seconds.'
    
    if slowmode_rate < 0 or slowmode_rate > 21600:
        return f'Slowmode can be min 0 and max 21600, got `{slowmode_rate}` seconds..'
    
    try:
        await ctx.client.channel_edit(ctx.channel, slowmode=slowmode_rate)
    except DiscordException as err:
        return f'Error setting channel\'s slowmode to `{slowmode_rate}` seconds:\n{err}'
    
    return f'Successfully set slow mode rate to `{slowmode_rate}` seconds.'


# A command can have sub-commands, just like in command-line tools.
# Example `!upper` and `!upper sub`
@Sakuya.commands(name = 'upper')
async def upper_command():
    """This is main command."""
    return 'This is the main command!'


@upper_command.commands(name = 'sub')
async def sub_command():
    """This is the upper command's sub command"""
    return 'This is the sub-command.'


# Hata has a predefined help command, which might be a great help for the start.
Sakuya.commands(SubterraneanHelpCommand(), 'help')


# If command that doesn't exist is called `.command_processor.unknown_command` is triggered.
#
# unknown_command is unlike generic command, it always has set parameters that are passed to it.
# Also `return`-ed and `yield`-ed values are not forwarded, and if exception occurs error handlers are not called.
@Sakuya.command_processor.unknown_command
async def command_processor(client, message, command_name):
    await client.message_create(message.channel, f'Could not find command named : {command_name!r}')


Sakuya.start()
