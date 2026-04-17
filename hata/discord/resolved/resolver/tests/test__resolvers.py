import vampytest

from ....message import Attachment, Message
from ....channel import Channel
from ....role import Role
from ....user import User

from ...resolved import Resolved

from ..resolvers import (
    RESOLVER_ATTACHMENT, RESOLVER_CHANNEL, RESOLVER_MENTIONABLE, RESOLVER_MESSAGE, RESOLVER_ROLE,
    RESOLVER_STRING, RESOLVER_USER
)


def _iter_options():
    yield (
        RESOLVER_STRING.resolve_single,
        False,
        None,
        None,
        None,
    )
    
    yield (
        RESOLVER_STRING.resolve_single,
        False,
        None,
        'shrimp',
        'shrimp',
    )
    
    
    yield (
        RESOLVER_STRING.iter_resolve_single,
        True,
        None,
        None,
        [],
    )
    
    yield (
        RESOLVER_STRING.iter_resolve_single,
        True,
        None,
        'shrimp',
        ['shrimp'],
    )
    
    yield (
        RESOLVER_STRING.resolve_multiple,
        False,
        None,
        None,
        None,
    )
    
    yield (
        RESOLVER_STRING.resolve_multiple,
        False,
        None,
        ('shrimp', 'fry'),
        ('shrimp', 'fry'),
    )
    
    
    yield (
        RESOLVER_STRING.iter_resolve_multiple,
        True,
        None,
        None,
        [],
    )
    
    yield (
        RESOLVER_STRING.iter_resolve_multiple,
        True,
        None,
        ('shrimp', 'fry'),
        ['shrimp', 'fry'],
    )
    
    
    attachment_0 = Attachment.precreate(202509120000)
    attachment_1 = Attachment.precreate(202509120001)
    channel_0 = Channel.precreate(202509120002)
    channel_1 = Channel.precreate(202509120003)
    message_0 = Message.precreate(202509120004)
    message_1 = Message.precreate(202509120005)
    role_0 = Role.precreate(202509120006)
    role_1 = Role.precreate(202509120007)
    user_0 = User.precreate(202509120008)
    user_1 = User.precreate(202509120009)
    
    for resolver, entities_parameter_name, entity_0, entity_1 in (
        (
            RESOLVER_ATTACHMENT,
            'attachments',
            attachment_0,
            attachment_1,
        ),
        (
            RESOLVER_CHANNEL,
            'channels',
            channel_0,
            channel_1,
        ),
        (
            RESOLVER_MESSAGE,
            'messages',
            message_0,
            message_1,
        ),
        (
            RESOLVER_ROLE,
            'roles',
            role_0,
            role_1,
        ),
        (
            RESOLVER_USER,
            'users',
            user_0,
            user_1,
        ),
        (
            RESOLVER_MENTIONABLE,
            'roles',
            role_0,
            role_1,
        ),
        (
            RESOLVER_MENTIONABLE,
            'users',
            user_0,
            user_1,
        ),
    ):
        yield (
            resolver.resolve_single,
            False,
            None,
            None,
            None,
        )
        
        yield (
            resolver.resolve_single,
            False,
            Resolved(**{
                entities_parameter_name: [entity_0, entity_1],
            }),
            None,
            None,
        )
        
        yield (
            resolver.resolve_single,
            False,
            None,
            str(entity_0.id),
            None,
        )
        
        yield (
            resolver.resolve_single,
            False,
            Resolved(**{
                entities_parameter_name: [entity_0, entity_1],
            }),
            None,
            None,
        )
        
        yield (
            resolver.resolve_single,
            False,
            Resolved(**{
                entities_parameter_name: [entity_0, entity_1],
            }),
            str(entity_0.id),
            entity_0,
        )
        
        
        yield (
            resolver.iter_resolve_single,
            True,
            None,
            None,
            [],
        )
        
        yield (
            resolver.iter_resolve_single,
            True,
            Resolved(**{
                entities_parameter_name: [entity_0, entity_1],
            }),
            None,
            [],
        )
        
        yield (
            resolver.iter_resolve_single,
            True,
            None,
            str(entity_0.id),
            [],
        )
        
        yield (
            resolver.iter_resolve_single,
            True,
            Resolved(**{
                entities_parameter_name: [entity_0, entity_1],
            }),
            None,
            [],
        )
        
        yield (
            resolver.iter_resolve_single,
            True,
            Resolved(**{
                entities_parameter_name: [entity_0, entity_1],
            }),
            str(entity_0.id),
            [entity_0],
        )
        
        
        yield (
            resolver.resolve_multiple,
            False,
            None,
            None,
            None,
        )
        
        yield (
            resolver.resolve_multiple,
            False,
            Resolved(**{
                entities_parameter_name: [entity_0, entity_1],
            }),
            None,
            None,
        )
        
        yield (
            resolver.resolve_multiple,
            False,
            None,
            (str(entity_0.id), str(entity_1.id)),
            None,
        )
        
        yield (
            resolver.resolve_multiple,
            False,
            Resolved(**{
                entities_parameter_name: [entity_0, entity_1],
            }),
            None,
            None,
        )
        
        yield (
            resolver.resolve_multiple,
            False,
            Resolved(**{
                entities_parameter_name: [entity_0, entity_1],
            }),
            (str(entity_0.id), str(entity_1.id)),
            (entity_0, entity_1),
        )
        
        
        yield (
            resolver.iter_resolve_multiple,
            True,
            None,
            None,
            [],
        )
        
        yield (
            resolver.iter_resolve_multiple,
            True,
            Resolved(**{
                entities_parameter_name: [entity_0, entity_1],
            }),
            None,
            [],
        )
        
        yield (
            resolver.iter_resolve_multiple,
            True,
            None,
            (str(entity_0.id), str(entity_1.id)),
            [],
        )
        
        yield (
            resolver.iter_resolve_multiple,
            True,
            Resolved(**{
                entities_parameter_name: [entity_0, entity_1],
            }),
            None,
            [],
        )
        
        yield (
            resolver.iter_resolve_multiple,
            True,
            Resolved(**{
                entities_parameter_name: [entity_0, entity_1],
            }),
            (str(entity_0.id), str(entity_1.id)),
            [entity_0, entity_1],
        )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__resolvers(resolver_function, resolver_is_generator, resolved, value_or_values):
    """
    Tests whether the given resolver function works as intended.
    
    Parameters
    ----------
    resolver_function ``FunctionType | GeneratorFunctionType``
        Resolver function to test.
    
    resolver_is_generator : ``bool`
        Whether the resolver is a generator.
    
    resolved : ``None | Resolved``
        Resolved to test with.
    
    value_or_values : `None | str | tuple<str>`
        Value or values to pass to the resolver function.
    
    Returns
    -------
    output : `None | object | tuple<object> | list<object>``
    """
    output = resolver_function(resolved, value_or_values)
    if resolver_is_generator:
        output = [*output]
    
    return output
