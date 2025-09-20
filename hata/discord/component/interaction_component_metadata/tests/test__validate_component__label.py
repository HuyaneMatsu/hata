import vampytest

from ...component import ComponentType
from ...interaction_component import InteractionComponent

from ..fields import validate_component__label


def _iter_options__passing():
    interaction_component__text_input = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'fury',
    )
    
    interaction_component__string_select = InteractionComponent(
        ComponentType.string_select,
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
    
    yield (
        None,
        None,
    )
    
    yield (
        interaction_component__text_input,
        interaction_component__text_input,
    )
    
    yield (
        interaction_component__string_select,
        interaction_component__string_select,
    )
    
    yield (
        interaction_component__user_select,
        interaction_component__user_select,
    )
    
    yield (
        interaction_component__channel_select,
        interaction_component__channel_select,
    )
    
    yield (
        interaction_component__role_select,
        interaction_component__role_select,
    )
    
    yield (
        interaction_component__mentionable_select,
        interaction_component__mentionable_select,
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
    
    interaction_component__button = InteractionComponent(
        ComponentType.button,
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
    
    interaction_component__text_display = InteractionComponent(
        ComponentType.text_display,
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
    
    
    yield interaction_component__none
    yield interaction_component__row
    yield interaction_component__label
    yield interaction_component__button
    yield interaction_component__section
    yield interaction_component__text_display
    yield interaction_component__thumbnail_media
    yield interaction_component__media_gallery
    yield interaction_component__attachment_media
    yield interaction_component__separator
    yield interaction_component__container


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_component__label(input_value):
    """
    Tests whether ``validate_component__label`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``None | InteractionComponent``
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_component__label(input_value)
    vampytest.assert_instance(output, InteractionComponent, nullable = True)
    return output
