import vampytest

from ....message import Attachment

from ...interaction_event import InteractionEvent
from ...resolved import Resolved

from ..fields import put_resolved_into


def test__put_resolved_into():
    """
    Tests whether ``put_resolved_into`` works as intended.
    """
    entity_id = 202211050041
    guild_id = 202211050042
    interaction_event = InteractionEvent(guild_id = guild_id)
    resolved = Resolved(attachments = [Attachment.precreate(entity_id)])
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'resolved': {}}),
        (resolved, True, {'resolved': resolved.to_data(defaults = True, interaction_event = interaction_event)}),
    ):
        output = put_resolved_into(input_value, {}, defaults, interaction_event = interaction_event)
        vampytest.assert_eq(output, expected_output)
