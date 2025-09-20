import vampytest

from ...component import ComponentType
from ...interaction_component import InteractionComponent

from ..fields import validate_components__section


def _iter_options__passing():
    interaction_component__text_display = InteractionComponent(
        ComponentType.text_display,
    )
    
    yield (
        None,
        None,
    )
    
    yield (
        [],
        None,
    )
    
    yield (
        [
            interaction_component__text_display,
        ],
        (
            interaction_component__text_display,
        ),
    )


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    interaction_component__none = InteractionComponent(
        component_type = ComponentType.none,
    )
    
    interaction_component__row = InteractionComponent(
        component_type = ComponentType.row,
        components = [
            InteractionComponent(
                ComponentType.text_input,
                custom_id = 'koishi',
            ),
        ],
    )
    
    interaction_component__label = InteractionComponent(
        ComponentType.label,
        component = InteractionComponent(
            ComponentType.text_input,
            custom_id = 'koishi',
        ),
    )
    interaction_component__text_input = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'koishi',
    )
    
    interaction_component__string_select = InteractionComponent(
        ComponentType.string_select,
        custom_id = 'koishi',
    )
    
    interaction_component__button = InteractionComponent(
        ComponentType.button,
        custom_id = 'koishi',
    )
    
    interaction_component__user_select = InteractionComponent(
        ComponentType.user_select,
        custom_id = 'koishi',
    )
    
    interaction_component__channel_select = InteractionComponent(
        ComponentType.channel_select,
        custom_id = 'koishi',
    )
    
    interaction_component__role_select = InteractionComponent(
        ComponentType.role_select,
        custom_id = 'koishi',
    )
    
    interaction_component__mentionable_select = InteractionComponent(
        ComponentType.mentionable_select,
        custom_id = 'koishi',
    )
    
    interaction_component__section = InteractionComponent(
        component_type = ComponentType.section,
        components = [
            InteractionComponent(
                ComponentType.text_display,
            ),
        ],
    )
    
    interaction_component__thumbnail_media = InteractionComponent(
        ComponentType.thumbnail_media,
    )
    
    interaction_component__media_gallery = InteractionComponent(
        ComponentType.media_gallery,
    )
    
    interaction_component__attachment_media = InteractionComponent(
        ComponentType.attachment_media,
    )
    
    interaction_component__separator = InteractionComponent(
        ComponentType.separator,
    )
    
    interaction_component__container = InteractionComponent(
        component_type = ComponentType.container,
        components = [
            InteractionComponent(
                ComponentType.text_display,
            ),
        ],
    )
    
    yield [interaction_component__none]
    yield [interaction_component__row]
    yield [interaction_component__label]
    yield [interaction_component__text_input]
    yield [interaction_component__string_select]
    yield [interaction_component__button]
    yield [interaction_component__user_select]
    yield [interaction_component__channel_select]
    yield [interaction_component__role_select]
    yield [interaction_component__mentionable_select]
    yield [interaction_component__section]
    yield [interaction_component__thumbnail_media]
    yield [interaction_component__media_gallery]
    yield [interaction_component__attachment_media]
    yield [interaction_component__separator]
    yield [interaction_component__container]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_components__section(input_value):
    """
    Tests whether `validate_components__section` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``None | tuple<InteractionComponent>``
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_components__section(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, InteractionComponent)
    
    return output
