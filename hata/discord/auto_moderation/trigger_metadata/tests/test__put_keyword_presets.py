import vampytest

from ..fields import put_keyword_presets
from ..preinstanced import AutoModerationKeywordPresetType


def _iter_options():
    yield None, False, {'presets': []}
    yield None, True, {'presets': []}
    yield (AutoModerationKeywordPresetType.slur, ), False, {'presets': [AutoModerationKeywordPresetType.slur.value]}
    yield (AutoModerationKeywordPresetType.slur, ), True, {'presets': [AutoModerationKeywordPresetType.slur.value]}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_keyword_presets(input_value, defaults):
    """
    Tests whether ``put_keyword_presets`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<AutoModerationKeywordPresetType>`
        Value to serialize.
    defaults : `bool`
        Whether fields with the default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_keyword_presets(input_value, {}, defaults)
