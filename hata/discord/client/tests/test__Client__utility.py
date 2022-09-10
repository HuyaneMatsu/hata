import vampytest

from ...channel import Channel, ChannelType
from ...core import USERS

from .. import Client


def test__Client__delete_0():
    """
    Issue: `User` alter ego was created of clients when the client was not yet finalized by startup at `Client._delete`.
    """
    client = Client('token_20220718')
    try:
        client._delete()
        vampytest.assert_not_in(client.id, USERS)
    finally:
        client = None


def test__Client__delete_1():
    """
    Counter check of ``test__Client__delete_0``.
    
    Alter ego should be created when a client is finalised at startup.
    """
    client = Client('token_20220718')
    try:
        # mark the client as finalised by setting it into `USERS`
        USERS[client.id] = client
        
        # Link the client to a group channel to keep the user in memory.
        channel = Channel.precreate(335788657879547922, channel_type = ChannelType.private_group)
        channel.users.append(client)
        client.group_channels[channel.id] = channel
        
        client._delete()
        vampytest.assert_in(client.id, USERS)
    finally:
        client = None


def test__Client__delete_2():
    """
    Issue: `TypeError` at `ChannelMetadataPrivateGroup._delete` when checking alter ego-s in private group channels.
    
    Test `test__Client__delete_1` might be the same, but we check different issues, so it is duplicated.
    """
    client = Client('token_20220718')
    try:
        # mark the client as finalised by setting it into `USERS`
        USERS[client.id] = client
        
        # Link the client to a group channel to keep the user in memory.
        channel = Channel.precreate(335788657879547921, channel_type = ChannelType.private_group)
        channel.users.append(client)
        client.group_channels[channel.id] = channel
        
        client._delete()
        vampytest.assert_in(client.id, USERS)
    finally:
        client = None
