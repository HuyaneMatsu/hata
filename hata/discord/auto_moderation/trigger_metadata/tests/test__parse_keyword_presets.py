import vampytest


from ..fields import parse_keyword_presets
from ..preinstanced import AutoModerationKeywordPresetType


def _iter_options():
    yield {}, None
    yield {'presets': None}, None
    yield {'presets': []}, None
    yield (
        {
            'presets': [
                AutoModerationKeywordPresetType.slur.value,
            ],
        },
        (
            AutoModerationKeywordPresetType.slur,
        ),
    )
    yield (
        {
            'presets': [
                AutoModerationKeywordPresetType.cursing.value,
                AutoModerationKeywordPresetType.slur.value,
            ],
        },
        (
            AutoModerationKeywordPresetType.cursing,
            AutoModerationKeywordPresetType.slur,
        ),
    )
    yield (
        {
            'presets': [
                AutoModerationKeywordPresetType.slur.value,
                AutoModerationKeywordPresetType.cursing.value,
            ],
        },
        (
            AutoModerationKeywordPresetType.cursing,
            AutoModerationKeywordPresetType.slur,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_keyword_presets(input_data):
    """
    Tests whether ``parse_keyword_presets`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<AutoModerationKeywordPresetType>`
    """
    output = parse_keyword_presets(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
