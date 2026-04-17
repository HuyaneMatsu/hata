import vampytest

from ..fields import parse_source_type
from ..preinstanced import EntitlementSourceType


def _iter_options():
    yield (
        {},
        EntitlementSourceType.none,
    )
    
    yield (
        {
            'source_type': None,
        },
        EntitlementSourceType.none,
    )
    
    yield (
        {
            'source_type': EntitlementSourceType.quest_reward.value,
        },
        EntitlementSourceType.quest_reward,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_source_type(input_data):
    """
    Tests whether ``parse_source_type`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``EntitlementSourceType``
    """
    output = parse_source_type(input_data)
    vampytest.assert_instance(output, EntitlementSourceType)
    return output
