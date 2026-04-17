import vampytest

from ...interaction_event import InteractionEvent

from ..context import InteractionResponseContext


def test__InteractionResponseContext__new():
    """
    Tests whether ``InteractionResponseContext.__new__`` works as intended.
    """
    deferring = False
    ephemeral = False
    interaction_event = InteractionEvent()
    
    context = InteractionResponseContext(
        interaction_event,
        deferring,
        ephemeral,
    )
    
    vampytest.assert_instance(context, InteractionResponseContext)
    
    vampytest.assert_eq(context.deferring, deferring)
    vampytest.assert_eq(context.ephemeral, ephemeral)
    vampytest.assert_is(context.interaction_event, interaction_event)
