import vampytest

from ...component import Component, ComponentType
from ...media_info import MediaInfo
from ...string_select_option import StringSelectOption

from ..fields import validate_components


def _iter_options__passing():
    component_row = Component(
        ComponentType.row,
        components = [
            Component(
                ComponentType.button,
                label = 'Orin',
            ),
        ],
    )
    
    component_label = Component(
        ComponentType.label,
        component = Component(
            ComponentType.text_input,
            placeholder = 'Fairies',
        ),
    )
    
    component_text_input = Component(
        ComponentType.text_input,
        placeholder = 'Fairies',
    )
    
    component_string_select = Component(
        ComponentType.string_select,
        options = [
            StringSelectOption('cart'),
        ],
    )
    
    component_text_display = Component(
        ComponentType.text_display,
        content = 'Orin',
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
            component_row,
        ],
        (
            component_row,
        ),
    )
    
    yield (
        [
            component_label,
        ],
        (
            component_label,
        ),
    )
    
    yield (
        [
            component_text_input,
        ],
        (
            Component(
                ComponentType.label,
                component = component_text_input,
            ),
        ),
    )
    
    yield (
        [
            component_string_select,
        ],
        (
            Component(
                ComponentType.label,
                component = component_string_select,
            ),
        ),
    )
    
    yield (
        [
            component_text_display,
        ],
        (
            component_text_display,
        ),
    )


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    component_none = Component(
        ComponentType.none,
    )
    
    component_button = Component(
        ComponentType.button,
        label = 'Orin',
    )
    
    component_thumbnail_media = Component(
        ComponentType.thumbnail_media,
        media = MediaInfo('attachment://orin.png'),
    )
    
    component_user_select = Component(
        ComponentType.user_select,
    )
    
    component_role_select = Component(
        ComponentType.role_select,
    )
    
    component_mentionable_select = Component(
        ComponentType.mentionable_select,
    )
    
    component_channel_select = Component(
        ComponentType.channel_select,
    )
    
    component_attachment_media = Component(
        ComponentType.attachment_media,
        media = MediaInfo('attachment://orin.png'),
    )
    
    component_separator = Component(
        ComponentType.separator,
    )
    
    component_section = Component(
        ComponentType.section,
        components = [
            Component(
                ComponentType.text_display,
                content = 'Orin',
            ),
        ],
    )
    
    yield [
        component_none,
    ]
    
    yield [
        component_button,
    ]
    
    yield [
        component_thumbnail_media,
    ]
    
    yield [
        component_user_select,
    ]
    
    yield [
        component_role_select,
    ]
    
    yield [
        component_mentionable_select,
    ]
    
    yield [
        component_channel_select,
    ]
    
    yield [
        component_attachment_media,
    ]
    
    yield [
        component_separator,
    ]
    
    yield [
        component_section,
    ]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_components(input_value):
    """
    Tests whether `validate_components` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``None | tuple<Component>``
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_components(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
