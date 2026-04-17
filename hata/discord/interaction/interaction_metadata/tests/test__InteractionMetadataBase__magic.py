import vampytest

from ..base import InteractionMetadataBase


def test__InteractionMetadataBase__repr():
    """
    Tests whether ``InteractionMetadataBase.__repr__`` works as intended.
    """
    interaction_metadata = InteractionMetadataBase()
    vampytest.assert_instance(repr(interaction_metadata), str)


def test__InteractionMetadataBase__hash():
    """
    Tests whether ``InteractionMetadataBase.__hash__`` works as intended.
    """
    interaction_metadata = InteractionMetadataBase()
    vampytest.assert_instance(hash(interaction_metadata), int)


def test__InteractionMetadataBase__eq__different_type():
    """
    Tests whether ``InteractionMetadataBase.__eq__`` works as intended.
    
    Case: different type.
    """
    interaction_metadata = InteractionMetadataBase()
    vampytest.assert_ne(interaction_metadata, object())


def _iter_options__eq():
    keyword_parameters = {}
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    

@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__InteractionMetadataBase__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``InteractionMetadataBase.__eq__`` works as intended.
    
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
    interaction_metadata_0 = InteractionMetadataBase(**keyword_parameters_0)
    interaction_metadata_1 = InteractionMetadataBase(**keyword_parameters_1)
    
    output = interaction_metadata_0 == interaction_metadata_1
    vampytest.assert_instance(output, bool)
    return output
