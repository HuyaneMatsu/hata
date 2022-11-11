import vampytest

from ...interaction_component import InteractionComponent

from ..form_submit import InteractionMetadataFormSubmit


def test__InteractionMetadataFormSubmit__iter_components():
    """
    Tests whether ``InteractionMetadataFormSubmit.iter_components`` works as intended.
    """
    interaction_component_1 = InteractionComponent(custom_id = 'negative')
    interaction_component_2 = InteractionComponent(custom_id = 'number')
    
    for interaction_component, expected_output in (
        (InteractionMetadataFormSubmit(components = None), []),
        (InteractionMetadataFormSubmit(components = [interaction_component_1]), [interaction_component_1]),
        (
            InteractionMetadataFormSubmit(components = [interaction_component_2, interaction_component_1]),
            [interaction_component_2, interaction_component_1]
        ),
    ):
        vampytest.assert_eq([*interaction_component.iter_components()], expected_output)


def test__InteractionMetadataFormSubmit__iter_custom_ids_and_values():
    """
    Tests whether ``InteractionMetadataFormSubmit.iter_custom_ids_and_values`` works as intended.
    """
    interaction_component_1 = InteractionComponent(custom_id = 'negative', value = 'ho')
    interaction_component_2 = InteractionComponent(custom_id = 'number', value = 'lo')
    interaction_component_3 = InteractionComponent()
    interaction_component_4 = InteractionComponent(
        custom_id = 'enclosed', value = 'dancehall', components = [interaction_component_1, interaction_component_2]
    )
    interaction_component_5 = InteractionComponent(
        components = [interaction_component_1, interaction_component_3]
    )
    
    for interaction_component, expected_output in (
        (interaction_component_1, {'negative': 'ho'}),
        (interaction_component_2, {'number': 'lo'}),
        (interaction_component_3, {}),
        (interaction_component_4, {'negative': 'ho', 'number': 'lo', 'enclosed': 'dancehall'}),
        (interaction_component_5, {'negative': 'ho'}),
    ):
        interaction_metadata = InteractionMetadataFormSubmit(components = [interaction_component])
        vampytest.assert_eq(dict(interaction_metadata.iter_custom_ids_and_values()), expected_output)


def test__InteractionMetadataFormSubmit__get_custom_id_value_relation():
    """
    Tests whether ``InteractionMetadataFormSubmit.get_custom_id_value_relation`` works as intended.
    """
    interaction_component_1 = InteractionComponent(custom_id = 'negative', value = 'ho')
    interaction_component_2 = InteractionComponent(custom_id = 'number', value = None)
    interaction_component_3 = InteractionComponent()
    interaction_component_4 = InteractionComponent(
        custom_id = 'enclosed', value = 'dancehall', components = [interaction_component_1, interaction_component_2]
    )
    interaction_component_5 = InteractionComponent(
        components = [interaction_component_1, interaction_component_3]
    )
    
    for interaction_component, expected_output in (
        (interaction_component_1, {'negative': 'ho'}),
        (interaction_component_2, {}),
        (interaction_component_3, {}),
        (interaction_component_4, {'negative': 'ho', 'enclosed': 'dancehall'}),
        (interaction_component_5, {'negative': 'ho'}),
    ):
        interaction_metadata = InteractionMetadataFormSubmit(components = [interaction_component])
        vampytest.assert_eq(interaction_metadata.get_custom_id_value_relation(), expected_output)


def test__InteractionMetadataFormSubmit__get_value_for():
    """
    Tests whether ``InteractionMetadataFormSubmit.get_value_for`` works as intended.
    """
    interaction_metadata = InteractionMetadataFormSubmit(
        components = [
            InteractionComponent(
                custom_id = 'inside',
                value = 'your mind',
                components = [
                    InteractionComponent(custom_id = 'Ran', value = None),
                    InteractionComponent(custom_id = 'Chen', value = 'Yakumo'),
                ],  
            ),  
        ],
    )
    
    vampytest.assert_is(interaction_metadata.get_value_for('Ran'), None)
    vampytest.assert_is(interaction_metadata.get_value_for('Chen'), 'Yakumo')
    vampytest.assert_is(interaction_metadata.get_value_for('Yukari'), None)


def test__InteractionMetadataFormSubmit__get_match_and_value():
    """
    Tests whether ``InteractionMetadataFormSubmit.get_match_and_value`` works as intended.
    """
    interaction_metadata = InteractionMetadataFormSubmit(
        components = [
            InteractionComponent(
                custom_id = 'inside',
                value = 'your mind',
                components = [
                    InteractionComponent(custom_id = 'Ran', value = None),
                    InteractionComponent(custom_id = 'Chen', value = 'Yakumo'),
                ],  
            ),  
        ],
    )
    
    vampytest.assert_eq(
        interaction_metadata.get_match_and_value(lambda custom_id: 'custom_id' if custom_id == 'Ran' else None),
        ('custom_id', None)
    )

    vampytest.assert_eq(
        interaction_metadata.get_match_and_value(lambda custom_id: 'custom_id' if custom_id == 'Chen' else None),
        ('custom_id', 'Yakumo')
    )
    
    vampytest.assert_eq(
        interaction_metadata.get_match_and_value(lambda custom_id: 'custom_id' if custom_id == 'Yukari' else None),
        (None, None)
    )


def test__InteractionMetadataFormSubmit__iter_matches_and_values():
    """
    Tests whether ``InteractionMetadataFormSubmit.iter_matches_and_values`` works as intended.
    """
    interaction_metadata = InteractionMetadataFormSubmit(
        components = [
            InteractionComponent(
                custom_id = 'inside',
                value = 'your mind',
                components = [
                    InteractionComponent(custom_id = 'Ran', value = None),
                    InteractionComponent(custom_id = 'Chen', value = 'Yakumo'),
                ],  
            ),  
        ],
    )
    
    vampytest.assert_eq(
        [*interaction_metadata.iter_matches_and_values(lambda custom_id: 'custom_id' if 'e' in custom_id else None)],
        [('custom_id', 'your mind'), ('custom_id', 'Yakumo')],
    )

    vampytest.assert_eq(
        [*interaction_metadata.iter_matches_and_values(lambda custom_id: 'Ran' if custom_id == 'Ran' else None)],
        [('Ran', None)],
    )
