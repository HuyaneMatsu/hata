import vampytest

from ...channel import Channel
from ...guild import Guild
from ...role import Role
from ...user import User

from ..proxy import AllowedMentionProxy
from ..utils import parse_allowed_mentions


def _iter_options__passing():
    yield (
        None,
        {'parse': []},
    )
    
    yield (
        AllowedMentionProxy('users'),
        {'parse': ['users']},
    )
    
    yield (
        (),
        {'parse': []},
    )
    
    yield (
        set(),
        {'parse': []},
    )
    
    yield (
        [],
        {'parse': []},
    )
    
    yield (
        ['users'],
        {'parse': ['users']},
    )
    
    yield (
        ['roles'],
        {'parse': ['roles']},
    )
    
    yield (
        ['everyone'],
        {'parse': ['everyone']},
    )
    
    yield (
        ['users', 'roles', 'everyone'],
        {'parse': ['everyone', 'users', 'roles']},
    )
    
    yield (
        [User.precreate(202402150000)],
        {'users': [str(202402150000)]},
    )
    
    yield (
        [User.precreate(202402150001), User.precreate(202402150002)],
        {'users': [str(202402150001), str(202402150002)]},
    )
    
    yield (
        [Role.precreate(202402150003)],
        {'roles': [str(202402150003)]},
    )
    
    yield (
        [Role.precreate(202402150004), Role.precreate(202402150005)],
        {'roles': [str(202402150004), str(202402150005)]},
    )
    
    yield (
        [User.precreate(202402150007), 'users'],
        {'parse': ['users']},
    )
    
    yield (
        [Role.precreate(202402150008), 'roles'],
        {'parse': ['roles']},
    )
    
    yield (
        [User.precreate(202402150009), Role.precreate(202402150010)],
        {'users': [str(202402150009)], 'roles': [str(202402150010)]},
    )
    
    yield (
        ['replied_user'],
        {'replied_user': True},
    )
    
    yield (
        ['!replied_user'],
        {'replied_user': False},
    )


def _iter_options__type_error():
    yield object()
    yield [Channel.precreate(202402150006)]
    yield [Guild.precreate(202402150006)]
    yield [object()]


def _iter_options__value_error():
    yield ['mister']


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__parse_allowed_mentions(input_value):
    """
    Tests whether ``parse_allowed_mentions`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Allowed mentions to validate.
    
    Returns
    --------
    data : `dict<str, object>`
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = parse_allowed_mentions(input_value)
    vampytest.assert_instance(output, dict)
    return output
