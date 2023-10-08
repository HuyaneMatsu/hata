from hata import Client, Guild
from hata.ext.slash import setup_ext_slash

# Setting up the Client.
#
# If you are unsure what is happening here, I recommend going back to e10_slash_commands
TOKEN = ''

Sakuya = Client(TOKEN)

# This is another way to setup the slash extension.
# use_default_exception_handler allows us to disable the extension handler Hata comes with, and use our own.
# But, Hata does allow multiple extension handlers, so if you want to keep the default, you can leave it as True.
slash = setup_ext_slash(Sakuya, use_default_exception_handler = False)

MY_GUILD = Guild.precreate(12345)

@Sakuya.interactions(guild = MY_GUILD)
async def test(event):
    """
    Simple command, this is just used to test a error handler.
    """
    raise TypeError()

@slash.error
async def slash_error(client, interaction_event, command, exception):
    """
    Setting up a basic error handler
    When a slash command has an error, it'll go back to the Error Handler.

    It'll give:
        client              :   Client                                          | Client
        interaction_event   :   InteractionEvent                                | Event
        command             :   ComponentCommand, SlashCommand,                 | The command that was invoked
                                SlashCommandCategory,                           |
                                SlashCommandFunction,                           |
                                SlashCommandParameterAutoCompleter              |
                                FormSubmitCommand                               |
        exception           :   BaseException                                   | The exception that was raised

    This should return a boolean
    """
    handled = False
    if isinstance(exception, TypeError):
        # Telling the user the command raised an exception
        await client.interaction_response_message_create(interaction_event, "This command raised TypeError!")
        # This error was handled
        handled = True

    # Returning if it handled the error or not.
    #
    # If this returns false, Hata will try other error handlers
    # If the error isn't handled, it won't respond to the user and output the error in the terminal.
    return handled

Sakuya.start()
