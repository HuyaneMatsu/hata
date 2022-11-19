import vampytest


from ..fields import parse_keyword_presets
from ..preinstanced import AutoModerationKeywordPresetType


def test__parse_keyword_presets():
    """
    Tests whether ``parse_keyword_presets`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'presets': None}, None),
        ({'presets': []}, None),
        ({'presets': [AutoModerationKeywordPresetType.slur.value]}, (AutoModerationKeywordPresetType.slur,)),
    ):
        output = parse_keyword_presets(input_data)
        vampytest.assert_eq(output, expected_output)
