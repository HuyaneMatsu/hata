from ...... import Client


def test__SlashCommand__autocomplete():
    """
    Issue: `AttributeError` in `SlashCommand._add_autocomplete_function`.
    
    By: Al_Loiz [ICU]#5392.
    
    At: 2022-07-18
    """
    client = Client(
        token = 'token_20220718',
        extensions = 'slash',
    )
    
    try:
        @client.interactions
        async def command_1(value_1: str):
            pass
        
        @client.interactions
        async def command_2(value_2: str):
            pass
        
        # Act
        @command_1.autocomplete('value_1')
        @command_2.autocomplete('value_2')
        async def autocomplete_commands(value):
            pass
    
    # Cleanup
    finally:
        client._delete()
        client = None
