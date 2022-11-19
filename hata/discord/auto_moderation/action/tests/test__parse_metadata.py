import vampytest

from ...action_metadata import AutoModerationActionMetadataBase, AutoModerationActionMetadataTimeout

from ..fields import parse_metadata
from ..preinstanced import AutoModerationActionType


def test__parse_metadata():
    """
    Tests whether ``parse_metadata`` is working as intended.
    """
    metadata = AutoModerationActionMetadataTimeout(duration = 69)
    
    for input_data, metadata_type, expected_output in (
        ({}, AutoModerationActionType.none, AutoModerationActionMetadataBase()),
        ({'metadata': None}, AutoModerationActionType.timeout, AutoModerationActionMetadataTimeout()),
        ({'metadata': metadata.to_data(defaults = False)}, AutoModerationActionType.timeout, metadata),
    ):
        metadata = parse_metadata(input_data, metadata_type)
        vampytest.assert_eq(metadata, expected_output)
