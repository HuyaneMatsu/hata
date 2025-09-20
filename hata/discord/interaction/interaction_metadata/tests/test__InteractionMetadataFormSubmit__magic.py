import vampytest

from ....component import ComponentType, InteractionComponent

from ..form_submit import InteractionMetadataFormSubmit


def test__InteractionMetadataFormSubmit__repr():
    """
    Tests whether ``InteractionMetadataFormSubmit.__repr__`` works as intended.
    """
    custom_id = 'Inaba'
    components = [
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'Rem',
        ),
    ]
    
    interaction_metadata = InteractionMetadataFormSubmit(
        custom_id = custom_id,
        components = components,
    )
    vampytest.assert_instance(repr(interaction_metadata), str)


def test__InteractionMetadataFormSubmit__hash():
    """
    Tests whether ``InteractionMetadataFormSubmit.__hash__`` works as intended.
    """
    custom_id = 'Inaba'
    components = [
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'Rem',
        )
    ]
    
    interaction_metadata = InteractionMetadataFormSubmit(
        custom_id = custom_id,
        components = components,
    )
    vampytest.assert_instance(hash(interaction_metadata), int)


def test__InteractionMetadataFormSubmit__different_type():
    """
    Tests whether ``InteractionMetadataFormSubmit.__eq__`` works as intended.
    
    Case: different type.
    """
    interaction_metadata = InteractionMetadataFormSubmit()
    vampytest.assert_ne(interaction_metadata, object())


def _iter_options__eq():
    custom_id = 'Inaba'
    components = [
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'Rem',
        ),
    ]
    
    keyword_parameters = {
        'custom_id': custom_id,
        'components': components,
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
            'custom_id': 'Reisen',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'components': None,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__InteractionMetadataFormSubmit__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``InteractionMetadataFormSubmit.__eq__`` works as intended.
    
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
    interaction_metadata_0 = InteractionMetadataFormSubmit(**keyword_parameters_0)
    interaction_metadata_1 = InteractionMetadataFormSubmit(**keyword_parameters_1)
    
    output = interaction_metadata_0 == interaction_metadata_1
    vampytest.assert_instance(output, bool)
    return output

    
