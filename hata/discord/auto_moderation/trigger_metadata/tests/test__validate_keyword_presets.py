import vampytest

from ..fields import validate_keyword_presets
from ..preinstanced import AutoModerationKeywordPresetType


def test__validate_keyword_presets__0():
    """
    Tests whether `validate_keyword_presets` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ([], None),
        (AutoModerationKeywordPresetType.slur, (AutoModerationKeywordPresetType.slur, )),
        (AutoModerationKeywordPresetType.slur.value, (AutoModerationKeywordPresetType.slur, )),
        ([AutoModerationKeywordPresetType.slur], (AutoModerationKeywordPresetType.slur, )),
        ([AutoModerationKeywordPresetType.slur.value], (AutoModerationKeywordPresetType.slur, )),
    ):
        output = validate_keyword_presets(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_keyword_presets__1():
    """
    Tests whether `validate_keyword_presets` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_keyword_presets(input_value)
