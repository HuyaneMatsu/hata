import vampytest

from ..base import ScheduledEventEntityMetadataBase


def _assert_fields_set(entity_metadata):
    """
    Tests whether all attributes of an ``ScheduledEventEntityMetadataBase`` are set.
    
    Parameters
    ----------
    entity_metadata : ``ScheduledEventEntityMetadataBase``
        The entity detail to check out.
    """
    vampytest.assert_instance(entity_metadata, ScheduledEventEntityMetadataBase)


def test__ScheduledEventEntityMetadataBase__new__no_fields():
    """
    Tests whether ``ScheduledEventEntityMetadataBase.__new__`` works as intended.
    
    Case: No fields given.
    """
    entity_metadata = ScheduledEventEntityMetadataBase()
    _assert_fields_set(entity_metadata)


def test__ScheduledEventEntityMetadataBase__from_keyword_parameters__no_fields():
    """
    Tests whether ``ScheduledEventEntityMetadataBase.from_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    keyword_parameters = {}
    
    entity_metadata = ScheduledEventEntityMetadataBase.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(entity_metadata)
    vampytest.assert_eq(keyword_parameters, {})


def test__ScheduledEventEntityMetadataBase__create_empty():
    """
    Tests whether ``ScheduledEventEntityMetadataBase._create_empty`` works as intended.
    """
    entity_metadata = ScheduledEventEntityMetadataBase._create_empty()
    _assert_fields_set(entity_metadata)
