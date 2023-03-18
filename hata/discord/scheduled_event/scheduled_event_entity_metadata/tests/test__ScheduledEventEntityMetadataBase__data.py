import vampytest

from ..base import ScheduledEventEntityMetadataBase

from .test__ScheduledEventEntityMetadataBase__constructor import _assert_fields_set


def test__ScheduledEventEntityMetadataBase__from_data__0():
    """
    Tests whether ``ScheduledEventEntityMetadataBase.from_data`` works as intended.
    
    Case: non-discord entity.
    """
    data = {}
    
    entity_metadata = ScheduledEventEntityMetadataBase.from_data(data)
    
    _assert_fields_set(entity_metadata)


def test__ScheduledEventEntityMetadataBase__to_data():
    """
    Tests whether ``ScheduledEventEntityMetadataBase.to_data`` works as intended.
    
    Case: defaults.
    """
    entity_metadata = ScheduledEventEntityMetadataBase()
    
    expected_data = {}
    
    vampytest.assert_eq(
        entity_metadata.to_data(
            defaults = True,
        ),
        expected_data,
    )
