import vampytest

from ....user import User

from ...embedded_activity_location import EmbeddedActivityLocation
from ...embedded_activity_user_state import EmbeddedActivityUserState

from ..embedded_activity import EmbeddedActivity


def test__EmbeddedActivity__repr():
    """
    Tests whether ``EmbeddedActivity.__repr__`` works as intended.
    """
    embedded_activity_id = 202408020070
    application_id = 202408020071
    guild_id = 202408020072
    launch_id = 202408020073
    location = EmbeddedActivityLocation(channel_id = 202408020074)
    user_states = [
         EmbeddedActivityUserState(user = User.precreate(202408020075)),
         EmbeddedActivityUserState(user = User.precreate(202408020076)),
    ]
    
    embedded_activity = EmbeddedActivity.precreate(
        embedded_activity_id,
        application_id = application_id,
        guild_id = guild_id,
        launch_id = launch_id,
        location = location,
        user_states = user_states,
    )
    
    output = repr(embedded_activity)
    vampytest.assert_instance(output, str)


def test__EmbeddedActivity__hash():
    """
    Tests whether ``EmbeddedActivity.__hash__`` works as intended.
    """
    embedded_activity_id = 202408020077
    application_id = 202408020078
    guild_id = 202408020079
    launch_id = 202408020080
    location = EmbeddedActivityLocation(channel_id = 202408020081)
    user_states = [
         EmbeddedActivityUserState(user = User.precreate(202408020082)),
         EmbeddedActivityUserState(user = User.precreate(202408020083)),
    ]
    
    embedded_activity = EmbeddedActivity.precreate(
        embedded_activity_id,
        application_id = application_id,
        guild_id = guild_id,
        launch_id = launch_id,
        location = location,
        user_states = user_states,
    )
    
    output = repr(embedded_activity)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    application_id = 202408020084
    location = EmbeddedActivityLocation(channel_id = 202408020085)
    
    keyword_parameters = {
        'application_id': application_id,
        'location': location,
    }
    
    yield (
        {},
        {},
        True,
    )
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'application_id': 202408020086,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'location': EmbeddedActivityLocation(channel_id = 202408020087),
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__EmbeddedActivity__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``EmbeddedActivity.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    embedded_activity_0 = EmbeddedActivity(**keyword_parameters_0)
    embedded_activity_1 = EmbeddedActivity(**keyword_parameters_1)
    
    output = embedded_activity_0 == embedded_activity_1
    vampytest.assert_instance(output, bool)
    return output


def test__EmbeddedActivity__eq__with_id():
    """
    Tests whether ``EmbeddedActivity.__eq__`` works as intended.
    
    Case: instances have their own identifiers.
    """
    embedded_activity_id_0 = 202408020088
    embedded_activity_id_1 = 202408020089
    
    application_id_0 = 202408020090
    application_id_1 = 202408020091
    
    embedded_activity_0 = EmbeddedActivity.precreate(embedded_activity_id_0, application_id = application_id_0)
    embedded_activity_1 = EmbeddedActivity.precreate(embedded_activity_id_1, application_id = application_id_1)
    embedded_activity_2 = EmbeddedActivity(application_id = application_id_0)
    
    vampytest.assert_eq(embedded_activity_0, embedded_activity_0)
    vampytest.assert_ne(embedded_activity_0, embedded_activity_1)
    vampytest.assert_eq(embedded_activity_0, embedded_activity_2)
    vampytest.assert_ne(embedded_activity_1, embedded_activity_2)
