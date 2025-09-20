import vampytest

from ...component_metadata import ComponentMetadataBase

from ..base import InteractionComponentMetadataBase


def test__InteractionComponentMetadataBase__repr():
    """
    Tests whether ``InteractionComponentMetadataBase.__repr__`` works as intended.
    """
    interaction_component_metadata = InteractionComponentMetadataBase()
    
    output = repr(interaction_component_metadata)
    vampytest.assert_instance(output, str)


def test__InteractionComponentMetadataBase__hash():
    """
    Tests whether ``InteractionComponentMetadataBase.__hash__`` works as intended.
    """
    interaction_component_metadata = InteractionComponentMetadataBase()
    
    output = hash(interaction_component_metadata)
    vampytest.assert_instance(output, int)


def test__InteractionComponentMetadataBase__eq__different_type():
    """
    Tests whether ``InteractionComponentMetadataBase.__eq__`` works as intended.
    
    Case: different type.
    """
    interaction_component_metadata = InteractionComponentMetadataBase()
    
    vampytest.assert_ne(interaction_component_metadata, object())


def _iter_options__eq():
    keyword_parameters = {}
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__InteractionComponentMetadataBase__eq__same_type(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``InteractionComponentMetadataBase.__eq__`` works as intended.
    
    Case: same type.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create from.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance from.
    
    Returns
    -------
    output : `bool`
    """
    interaction_component_metadata_0 = InteractionComponentMetadataBase(**keyword_parameters_0)
    interaction_component_metadata_1 = InteractionComponentMetadataBase(**keyword_parameters_1)
    
    output = interaction_component_metadata_0 == interaction_component_metadata_1
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__match_to_component():
    yield (
        {},
        ComponentMetadataBase(),
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__match_to_component()).returning_last())
def test__InteractionComponentMetadataBase__match_to_component(keyword_parameters, component_metadata):
    """
    Tests whether ``InteractionComponentMetadataBase._match_to_component`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    component_metadata : ``ComponentMetadataBase``
        Component metadata to test with.
    
    Returns
    -------
    output : `bool`
    """
    interaction_component_metadata = InteractionComponentMetadataBase(**keyword_parameters)
    
    output = interaction_component_metadata._match_to_component(component_metadata)
    vampytest.assert_instance(output, bool)
    return output
