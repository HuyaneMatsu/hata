import vampytest

from ....core import BUILTIN_EMOJIS

from ...activity import Activity, ActivityType

from ..preinstanced import _name_getter_custom, ACTIVITY_NAME_HANGING_DEFAULT


def _iter_options():
    emoji = BUILTIN_EMOJIS['x']
    text = 'miau'
    
    yield (
        Activity('', activity_type = ActivityType.hanging),
        ACTIVITY_NAME_HANGING_DEFAULT,
    )
    
    yield (
        Activity('', activity_type = ActivityType.hanging, emoji = emoji),
        emoji.as_emoji,
    )
    
    yield (
        Activity('', activity_type = ActivityType.hanging, details = text),
        text,
    )
    
    yield (
        Activity('', activity_type = ActivityType.hanging, details = text, emoji = emoji),
        f'{emoji} {text}',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__name_getter_custom(activity):
    """
    Tests whether ``_name_getter_custom`` works as intended.
    
    Parameters
    ----------
    activity : ``Activity``
        The activity to test on.
    
    Returns
    -------
    output : `str`
    """
    output = _name_getter_custom(activity)
    vampytest.assert_instance(output, str)
    return output
