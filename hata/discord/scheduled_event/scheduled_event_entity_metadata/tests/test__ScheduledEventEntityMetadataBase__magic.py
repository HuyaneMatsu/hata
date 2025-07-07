import vampytest

from ..base import ScheduledEventEntityMetadataBase


def test__ScheduledEventEntityMetadataBase__repr():
    """
    Tests whether ``ScheduledEventEntityMetadataBase.__new__`` works as intended.
    """
    entity_metadata = ScheduledEventEntityMetadataBase()
    
    vampytest.assert_instance(repr(entity_metadata), str)


def _iter_options__eq():
    keyword_parameters = {}
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ScheduledEventEntityMetadataBase__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ScheduledEventEntityMetadataBase.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    entity_metadata_0 = ScheduledEventEntityMetadataBase(**keyword_parameters_0)
    entity_metadata_1 = ScheduledEventEntityMetadataBase(**keyword_parameters_1)
    
    output = entity_metadata_0 == entity_metadata_1
    vampytest.assert_instance(output, bool)
    return output


def test__ScheduledEventEntityMetadataBase__hash():
    """
    Tests whether ``ScheduledEventEntityMetadataBase.__hash__`` works as intended.
    """
    entity_metadata = ScheduledEventEntityMetadataBase()
    
    vampytest.assert_instance(hash(entity_metadata), int)
