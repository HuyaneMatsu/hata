import vampytest

from ....discord import Client

from ..exceptions import default_slasher_random_error_message_getter
from ..slasher import Slasher



def test__Slasher__random_error_message_getter():
    """
    Tests whether ``Slasher.random_error_message_getter`` works as intended.
    """
    client_id = 202407210004
    
    client = Client(
        token = 'token_' + str(client_id),
        client_id = client_id,
    )
    
    slasher = Slasher(client)
    
    try:
        # get -> default
        output = slasher.random_error_message_getter
        vampytest.assert_is(output, default_slasher_random_error_message_getter)
        
        # set function -> not default
        random_error_message_getter = lambda : 'output'
        slasher.random_error_message_getter = random_error_message_getter
        output = slasher.random_error_message_getter
        vampytest.assert_is(output, random_error_message_getter)
    
        # set none -> default
        random_error_message_getter = None
        slasher.random_error_message_getter = random_error_message_getter
        output = slasher.random_error_message_getter
        vampytest.assert_is(output, default_slasher_random_error_message_getter)
        
        # set bad -> previous
        random_error_message_getter = lambda x: 'output'
        with vampytest.assert_raises(TypeError):
            slasher.random_error_message_getter = random_error_message_getter
        output = slasher.random_error_message_getter
        vampytest.assert_is(output, default_slasher_random_error_message_getter)
    finally:
        client._delete()
        client = None
