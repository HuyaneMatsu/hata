import vampytest

from ..string_select import InteractionComponentMetadataStringSelect


def _assert_fields_set(interaction_component_metadata):
    """
    Checks whether the ``InteractionComponentMetadataStringSelect`` has all it's attributes set.
    
    Parameters
    ----------
    interaction_component_metadata : ``InteractionComponentMetadataStringSelect``
        Component metadata to check.
    """
    vampytest.assert_instance(interaction_component_metadata, InteractionComponentMetadataStringSelect)
    vampytest.assert_instance(interaction_component_metadata.custom_id, str, nullable = True)
    vampytest.assert_instance(interaction_component_metadata.values, tuple, nullable = True)


def test__InteractionComponentMetadataStringSelect__new__no_fields():
    """
    Tests whether ``InteractionComponentMetadataStringSelect.__new__`` works as intended.
    
    Case: no fields given.
    """
    interaction_component_metadata = InteractionComponentMetadataStringSelect()
    _assert_fields_set(interaction_component_metadata)


def test__InteractionComponentMetadataStringSelect__new__all_fields():
    """
    Tests whether ``InteractionComponentMetadataStringSelect.__new__`` works as intended.
    
    Case: all fields given.
    """
    custom_id = 'koishi'
    values = ['oh', 'smart']
    
    interaction_component_metadata = InteractionComponentMetadataStringSelect(
        custom_id = custom_id,
        values = values,
    )
    _assert_fields_set(interaction_component_metadata)
    
    vampytest.assert_eq(interaction_component_metadata.custom_id, custom_id)
    vampytest.assert_eq(interaction_component_metadata.values, tuple(values))


def test__InteractionComponentMetadataStringSelect__from_keyword_parameters__no_fields():
    """
    Tests whether ``InteractionComponentMetadataStringSelect.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    interaction_component_metadata = InteractionComponentMetadataStringSelect.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(interaction_component_metadata)


def test__InteractionComponentMetadataStringSelect__from_keyword_parameters__all_fields():
    """
    Tests whether ``InteractionComponentMetadataStringSelect.from_keyword_parameters`` works as intended.
    
    Case: all fields given.
    """
    custom_id = 'koishi'
    values = ['oh', 'smart']
    
    keyword_parameters = {
        'custom_id': custom_id,
        'values': values,
    }
    
    interaction_component_metadata = InteractionComponentMetadataStringSelect.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(interaction_component_metadata)
    
    vampytest.assert_eq(interaction_component_metadata.custom_id, custom_id)
    vampytest.assert_eq(interaction_component_metadata.values, tuple(values))
