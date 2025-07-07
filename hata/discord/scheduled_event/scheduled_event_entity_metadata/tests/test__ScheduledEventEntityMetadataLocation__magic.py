import vampytest

from ..location import ScheduledEventEntityMetadataLocation


def test__ScheduledEventEntityMetadataLocation__repr():
    """
    Tests whether ``ScheduledEventEntityMetadataLocation.__new__`` works as intended.
    """
    location = 'Koishi WonderLand'
    
    entity_metadata = ScheduledEventEntityMetadataLocation(
        location = location,
    )
    
    vampytest.assert_instance(repr(entity_metadata), str)


def _iter_options__eq():
    location = 'Koishi WonderLand'
    
    keyword_parameters = {
        'location': location,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'location': 'Orin\'s dance house',
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ScheduledEventEntityMetadataLocation__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ScheduledEventEntityMetadataLocation.__eq__`` works as intended.
    
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
    entity_metadata_0 = ScheduledEventEntityMetadataLocation(**keyword_parameters_0)
    entity_metadata_1 = ScheduledEventEntityMetadataLocation(**keyword_parameters_1)
    
    output = entity_metadata_0 == entity_metadata_1
    vampytest.assert_instance(output, bool)
    return output


def test__ScheduledEventEntityMetadataLocation__hash():
    """
    Tests whether ``ScheduledEventEntityMetadataLocation.__hash__`` works as intended.
    """
    location = 'Koishi WonderLand'
    
    entity_metadata = ScheduledEventEntityMetadataLocation(
       location = location,
    )
    
    vampytest.assert_instance(hash(entity_metadata), int)
