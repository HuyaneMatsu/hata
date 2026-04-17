import vampytest

from ..fields import validate_keyword_presets
from ..preinstanced import AutoModerationKeywordPresetType


def _iter_options__passing():
    yield None, None
    yield [], None
    yield AutoModerationKeywordPresetType.slur, (AutoModerationKeywordPresetType.slur,)
    yield [AutoModerationKeywordPresetType.slur], (AutoModerationKeywordPresetType.slur, )
    yield AutoModerationKeywordPresetType.slur.value, (AutoModerationKeywordPresetType.slur,)
    yield [AutoModerationKeywordPresetType.slur.value], (AutoModerationKeywordPresetType.slur, )
    yield (
        [AutoModerationKeywordPresetType.cursing, AutoModerationKeywordPresetType.slur],
        (AutoModerationKeywordPresetType.cursing, AutoModerationKeywordPresetType.slur),
    )
    yield (
        [AutoModerationKeywordPresetType.slur, AutoModerationKeywordPresetType.cursing],
        (AutoModerationKeywordPresetType.cursing, AutoModerationKeywordPresetType.slur),
    )


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_keyword_presets(input_value):
    """
    Tests whether `validate_keyword_presets` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | tuple<AutoModerationKeywordPresetType>`
        Validated value.
    
    Raises
    ------
    TypeError
    """
    output = validate_keyword_presets(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
