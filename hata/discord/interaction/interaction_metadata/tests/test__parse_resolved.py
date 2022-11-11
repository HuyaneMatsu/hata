import vampytest

from ....message import Attachment

from ...interaction_event import InteractionEvent
from ...resolved import Resolved

from ..fields import parse_resolved


def test__parse_resolved():
    """
    Tests whether ``parse_resolved`` works as intended.
    """
    entity_id = 202211050039
    guild_id = 202211050040
    interaction_event = InteractionEvent(guild_id = guild_id)
    resolved = Resolved(attachments = [Attachment.precreate(entity_id)])
    
    for input_value, expected_output in (
        ({}, None),
        ({'resolved': None}, None),
        ({'resolved': {}}, None),
        ({'resolved': resolved.to_data(defaults = True, interaction_event = interaction_event)}, resolved),
    ):
        output = parse_resolved(input_value, interaction_event)
        vampytest.assert_eq(output, expected_output)
