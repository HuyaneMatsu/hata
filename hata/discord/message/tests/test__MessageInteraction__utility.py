import vampytest

from ...interaction import InteractionType
from ...user import ZEROUSER

from .. import MessageInteraction


def test__MessageInteraction__joined_name():
    """
    Tests whether ``MessageInteraction``'s `joined_name` property works as expected.
    """
    data = {
        'id': '2',
        'user': ZEROUSER.to_data(),
        'type': InteractionType.application_command.value,
    }
    
    for passed_name, joined_name in (
        (None, '',),
        ('name', 'name'),
        ('name sub command', 'name sub command'),
    ):
        data['name'] = passed_name
        message_interaction = MessageInteraction(data, 0)
        vampytest.assert_eq(message_interaction.joined_name, joined_name)
