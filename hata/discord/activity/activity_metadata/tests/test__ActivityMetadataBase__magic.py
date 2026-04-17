import vampytest

from ..base import ActivityMetadataBase


def test__ActivityMetadataBase__repr():
    """
    Tests whether ``ActivityMetadataBase.__repr__`` works as intended.
    """
    activity_metadata = ActivityMetadataBase()
    
    output = repr(activity_metadata)
    vampytest.assert_instance(output, str)


def test__ActivityMetadataBase__hash():
    """
    Tests whether ``ActivityMetadataBase.__hash__`` works as intended.
    """
    activity_metadata = ActivityMetadataBase()
    
    output = hash(activity_metadata)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    keyword_parameters = {}
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ActivityMetadataBase__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ActivityMetadataBase.__eq__`` works as intended.
    
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
    activity_metadata_base_0 = ActivityMetadataBase(**keyword_parameters_0)
    activity_metadata_base_1 = ActivityMetadataBase(**keyword_parameters_1)
    
    output = activity_metadata_base_0 == activity_metadata_base_1
    vampytest.assert_instance(output, bool)
    return output
