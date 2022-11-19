import vampytest

from ...action_metadata import AutoModerationActionMetadataBase, AutoModerationActionMetadataTimeout

from ..fields import put_metadata_into


def test__put_metadata_into():
    """
    Tests whether ``put_metadata_into`` is working as intended.
    """
    metadata = AutoModerationActionMetadataTimeout(duration = 69)
    
    for input_value, defaults, expected_output in (
        (AutoModerationActionMetadataBase(), False, {}),
        (AutoModerationActionMetadataBase(), True, {'metadata': {}}),
        (metadata, False, {'metadata': metadata.to_data(defaults = False)}),
    ):
        data = put_metadata_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
