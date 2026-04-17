import vampytest

from ..timeout import AutoModerationActionMetadataTimeout


def test__AutoModerationActionMetadataTimeout__eq__0():
    """
    Tests whether ``AutoModerationActionMetadataTimeout.__eq__` works as intended.
    """
    duration = 69
    
    keyword_parameters = {
        'duration': duration,
    }
    
    metadata = AutoModerationActionMetadataTimeout(**keyword_parameters)
    
    vampytest.assert_eq(metadata, metadata)
    vampytest.assert_ne(metadata, object())
    
    for field_name, field_value in (
        ('duration', 70),
    ):
        test_metadata = AutoModerationActionMetadataTimeout(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(metadata, test_metadata)


def test__AutoModerationActionMetadataTimeout__hash():
    """
    Tests whether ``AutoModerationActionMetadataTimeout.__hash__` works as intended.
    """
    duration = 69
    
    metadata = AutoModerationActionMetadataTimeout(duration)
    
    vampytest.assert_instance(hash(metadata), int)


def test__AutoModerationActionMetadataTimeout__repr():
    """
    Tests whether ``AutoModerationActionMetadataTimeout.__repr__` works as intended.
    """
    duration = 69
    
    metadata = AutoModerationActionMetadataTimeout(duration)
    
    vampytest.assert_instance(repr(metadata), str)
