import vampytest

from ... permission import Permission

from .. import Channel


def test__Channel__permissions_for_roles():
    """
    Tests whether `channel.permissions_for_roles` wont raise when called and returns the correct type.
    """
    channel = Channel.precreate(20220815)
    permission = channel.permissions_for_roles()
    vampytest.assert_instance(permission, Permission)


def test__Channel__get_users_like():
    """
    Tests whether `channel.get_users_like` wont raise when called and returns the correct type.
    """
    channel = Channel.precreate(20220815)
    users = channel.get_users_like('nanahira')
    vampytest.assert_instance(users, list)
