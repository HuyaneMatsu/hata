import vampytest

from ..fields import put_keyword_presets_into
from ..preinstanced import AutoModerationKeywordPresetType


def test__put_keyword_presets_into():
    """
    Tests whether ``put_keyword_presets_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {'presets': []}),
        ((AutoModerationKeywordPresetType.slur, ), True, {'presets': [AutoModerationKeywordPresetType.slur.value]}),
    ):
        data = put_keyword_presets_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
