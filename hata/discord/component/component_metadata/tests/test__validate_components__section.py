import vampytest

from ...component import Component, ComponentType
from ...media_info import MediaInfo
from ...string_select_option import StringSelectOption

from ..fields import validate_components__section


def _iter_options__passing():
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
    
    component_row = Component(
        ComponentType.row,
        components = [
            Component(
                ComponentType.button,
                label = 'Orin',
            ),
        ],
    )
    
    component_thumbnail_media = Component(
        ComponentType.thumbnail_media,
        media = MediaInfo('attachment://orin.png'),
    )
    
    component_attachment_media = Component(
        ComponentType.attachment_media,
        media = MediaInfo('attachment://orin.png'),
    )
    
    component_separator = Component(
        ComponentType.separator,
    )
    
    component_button = Component(
        ComponentType.button,
        label = 'Orin',
    )
    
    component_string_select = Component(
        ComponentType.string_select,
        options = [
            StringSelectOption('cart'),
        ],
    )

    component_text_input = Component(
        ComponentType.text_input,
        label = 'Fairies',
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
    
    component_section = Component(
        ComponentType.section,
        components = [
            Component(
                ComponentType.text_display,
                content = 'Orin',
            ),
        ],
    )
    
    component_text_display = Component(
        ComponentType.text_display,
        content = 'Orin',
    )
    
    component_label = Component(
        ComponentType.label,
        component = Component(
            ComponentType.text_input,
            placeholder = 'Orin',
        ),
    )
    
    yield [
        component_none,
    ]
    
    yield [
        component_row,
    ]
    
    yield [
        component_thumbnail_media,
    ]
    
    yield [
        component_attachment_media,
    ]
    
    yield [
        component_separator,
    ]
    
    yield [
        component_button,
    ]
    
    yield [
        component_string_select,
    ]
    
    yield [
        component_text_input,
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
        component_section,
    ]
    
    yield [
        component_label,
    ]
    
    # double nesting | cannot nest row into row
    yield (
        [
            [component_button],
        ],
    ),
    
    # double nesting | cannot nest text display into a row
    yield (
        [
            [component_text_display],
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_components__section(input_value):
    """
    Tests whether ``validate_components__section`` works as intended.
    
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
    output = validate_components__section(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
