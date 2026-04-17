import vampytest

from ...checkbox_group_option import CheckboxGroupOption
from ...component import Component, ComponentType
from ...media_info import MediaInfo
from ...radio_group_option import RadioGroupOption
from ...string_select_option import StringSelectOption

from ..fields import validate_component__label


def _iter_options__passing():
    component__text_input = Component(
        ComponentType.text_input,
        placeholder = 'Fairies',
    )
    
    component__string_select = Component(
        ComponentType.string_select,
        options = [
            StringSelectOption('cart'),
        ],
    )
    
    component__user_select = Component(
        ComponentType.user_select,
    )
    
    component__role_select = Component(
        ComponentType.role_select,
    )
    
    component__mentionable_select = Component(
        ComponentType.mentionable_select,
    )
    
    component__channel_select = Component(
        ComponentType.channel_select,
    )
    
    component__attachment_input = Component(
        ComponentType.attachment_input,
    )
    
    component__radio_group = Component(
        ComponentType.radio_group,
        options = [
            RadioGroupOption('cart'),
        ],
    )
    
    component__checkbox_group = Component(
        ComponentType.checkbox_group,
        options = [
            CheckboxGroupOption('cart'),
        ],
    )
    
    component__checkbox = Component(
        ComponentType.checkbox,
        default = True,
    )
    
    yield (
        None,
        None,
    )
    
    yield (
        component__text_input,
        component__text_input,
    )
    
    yield (
        component__string_select,
        component__string_select,
    )
    
    yield (
        component__user_select,
        component__user_select,
    )
    
    yield (
        component__role_select,
        component__role_select,
    )
    
    yield (
        component__mentionable_select,
        component__mentionable_select,
    )
    
    yield (
        component__channel_select,
        component__channel_select,
    )
    
    yield (
        component__attachment_input,
        component__attachment_input,
    )
    
    yield (
        component__radio_group,
        component__radio_group,
    )
    
    yield (
        component__checkbox_group,
        component__checkbox_group,
    )
    
    yield (
        component__checkbox,
        component__checkbox,
    )


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    component__none = Component(
        ComponentType.none,
    )
    
    component__row = Component(
        ComponentType.row,
        components = [
            Component(
                ComponentType.button,
                label = 'Orin',
            ),
        ],
    )
    
    component__attachment_media = Component(
        ComponentType.attachment_media,
        media = MediaInfo('attachment://orin.png'),
    )
    
    component__separator = Component(
        ComponentType.separator,
    )
    
    component__button = Component(
        ComponentType.button,
        label = 'Orin',
    )
    
    component__thumbnail_media = Component(
        ComponentType.thumbnail_media,
        media = MediaInfo('attachment://orin.png'),
    )
    
    component__text_display = Component(
        ComponentType.text_display,
        content = 'Orin',
    )
    
    component__label = Component(
        ComponentType.label,
        component = Component(
            ComponentType.text_input,
            placeholder = 'Orin',
        ),
    )
    
    yield component__none
    yield component__row
    yield component__attachment_media
    yield component__separator
    yield component__button
    yield component__thumbnail_media
    yield component__text_display
    yield component__label


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
    output : ``None | Component``
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_component__label(input_value)
    vampytest.assert_instance(output, Component, nullable = True)
    return output
