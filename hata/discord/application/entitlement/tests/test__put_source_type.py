import vampytest

from ..fields import put_source_type
from ..preinstanced import EntitlementSourceType


def _iter_options():
    yield (
        EntitlementSourceType.none,
        False,
        {
            'source_type': EntitlementSourceType.none.value,
        },
    )

    yield (
        EntitlementSourceType.none,
        True,
        {
            'source_type': EntitlementSourceType.none.value,
        },
    )
    
    yield (
        EntitlementSourceType.quest_reward,
        False,
        {
            'source_type': EntitlementSourceType.quest_reward.value,
        },
    )

    yield (
        EntitlementSourceType.quest_reward,
        True,
        {
            'source_type': EntitlementSourceType.quest_reward.value,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_source_type(input_value, defaults):
    """
    Tests whether ``put_source_type`` works as intended.
    
    Parameters
    ----------
    input_value : ``EntitlementSourceType``
        Input value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_source_type(input_value, {}, defaults)
