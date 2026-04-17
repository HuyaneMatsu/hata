from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....emoji import Emoji

from ..hanging import ActivityMetadataHanging
from ..preinstanced import HangType


def test__ActivityMetadataHanging__repr():
    """
    Tests whether ``ActivityMetadataHanging.__repr__`` works as intended.
    """
    created_at = DateTime(2014, 9, 16, tzinfo = TimeZone.utc)
    details = 'details'
    emoji = Emoji.precreate(202408310012, name = 'Code49')
    hang_type = HangType.custom
    
    activity_metadata = ActivityMetadataHanging(
        created_at = created_at,
        details = details,
        emoji = emoji,
        hang_type = hang_type,
    )
    
    vampytest.assert_instance(repr(activity_metadata), str)


def test__ActivityMetadataHanging__hash():
    """
    Tests whether ``ActivityMetadataHanging.__hash__`` works as intended.
    """
    created_at = DateTime(2014, 9, 16, tzinfo = TimeZone.utc)
    details = 'details'
    emoji = Emoji.precreate(202408310013, name = 'Code49')
    hang_type = HangType.custom
    
    activity_metadata = ActivityMetadataHanging(
        created_at = created_at,
        details = details,
        emoji = emoji,
        hang_type = hang_type,
    )
    
    vampytest.assert_instance(hash(activity_metadata), int)



def _iter_options__eq():
    created_at = DateTime(2014, 9, 16, tzinfo = TimeZone.utc)
    details = 'details'
    emoji = Emoji.precreate(202408310014, name = 'Code49')
    hang_type = HangType.custom
    
    keyword_parameters = {
        'created_at': created_at,
        'details': details,
        'emoji': emoji,
        'hang_type': hang_type,
    }
    
    yield (
        {},
        {},
        True
    )
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'created_at': None,
        },
        False
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'details': None,
        },
        False
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'emoji': None,
        },
        False
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'hang_type': HangType.gaming,
        },
        False
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ActivityMetadataHanging__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ActivityMetadataHanging.__eq__`` works as intended.
    
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
    activity_metadata_0 = ActivityMetadataHanging(**keyword_parameters_0)
    activity_metadata_1 = ActivityMetadataHanging(**keyword_parameters_1)
    
    output = activity_metadata_0 == activity_metadata_1
    vampytest.assert_instance(output, bool)
    return output
