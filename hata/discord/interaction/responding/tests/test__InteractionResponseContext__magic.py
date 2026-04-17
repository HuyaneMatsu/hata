import vampytest

from ...interaction_event import InteractionEvent

from ..context import InteractionResponseContext


def test__InteractionResponseContext__repr():
    """
    Tests whether ``InteractionResponseContext.__repr__`` works as intended.
    """
    deferring = False
    ephemeral = False
    interaction_event = InteractionEvent()
    
    context = InteractionResponseContext(
        interaction_event,
        deferring,
        ephemeral,
    )
    
    vampytest.assert_instance(repr(context), str)


def test__InteractionResponseContext__hash():
    """
    Tests whether ``InteractionResponseContext.__hash__`` works as intended.
    """
    deferring = False
    ephemeral = False
    interaction_event = InteractionEvent()
    
    context = InteractionResponseContext(
        interaction_event,
        deferring,
        ephemeral,
    )
    
    vampytest.assert_instance(hash(context), int)


def test__InteractionResponseContext__eq():
    """
    Tests whether ``InteractionResponseContext.__eq__`` works as intended.
    """
    deferring = False
    ephemeral = False
    interaction_event = InteractionEvent.precreate(202211090000)
    
    keyword_parameters = {
        'deferring': deferring,
        'ephemeral': ephemeral,
        'interaction_event': interaction_event,
    }
    
    context = InteractionResponseContext(**keyword_parameters)
    
    vampytest.assert_eq(context, context)
    vampytest.assert_ne(context, object())
    
    for field_name, field_value in (
        ('deferring', True),
        ('ephemeral', True),
        ('interaction_event', InteractionEvent.precreate(202211090001)),
    ):
        text_context = InteractionResponseContext(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(context, text_context)
