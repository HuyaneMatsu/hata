import vampytest

from ..checkbox_group_option import CheckboxGroupOption
from ..component import Component, ComponentType
from ..media_info import MediaInfo
from ..radio_group_option import RadioGroupOption
from ..shared_fields import validate_components
from ..string_select_option import StringSelectOption


def _iter_options__passing():
    component__button = Component(
        ComponentType.button,
        label = 'Orin',
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
    
    component__text_display = Component(
        ComponentType.text_display,
        content = 'Orin',
    )
    
    component__attachment_media = Component(
        ComponentType.attachment_media,
        media = MediaInfo('attachment://orin.png'),
    )
    
    component__separator = Component(
        ComponentType.separator,
    )
    
    component__section = Component(
        ComponentType.section,
        components = [
            Component(
                ComponentType.text_display,
                content = 'Orin',
            ),
        ],
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
            component__button,
        ],
        (
            component__button,
        ),
    )
    
    yield (
        [
            component__row,
        ],
        (
            component__row,
        ),
    )
    
    yield (
        [
            component__string_select,
        ],
        (
            component__string_select,
        ),
    )
    
    yield (
        [
            component__user_select,
        ],
        (
            component__user_select,
        ),
    )
    
    yield (
        [
            component__role_select,
        ],
        (
            component__role_select,
        ),
    )
    
    yield (
        [
            component__mentionable_select,
        ],
        (
            component__mentionable_select,
        )
    )
    
    yield (
        [
            component__channel_select,
        ],
        (
            component__channel_select,
        ),
    )
    
    yield (
        [
            component__text_display,
        ],
        (
            component__text_display,
        ),
    )
    
    yield (
        [
            component__attachment_media,
        ],
        (
            component__attachment_media,
        ),
    )
    
    yield (
        [
            component__separator,
        ],
        (
            component__separator,
        ),
    )
    
    yield (
        [
            component__section,
        ],
        (
            component__section,
        ),
    )


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    component__none = Component(
        ComponentType.none,
    )

    component__text_input = Component(
        ComponentType.text_input,
        placeholder = 'Fairies',
    )
    
    component__thumbnail_media = Component(
        ComponentType.thumbnail_media,
        media = MediaInfo('attachment://orin.png'),
    )
    
    component__button = Component(
        ComponentType.button,
        label = 'Orin',
    )
    
    component__text_display = Component(
        ComponentType.text_display,
        content = 'Orin',
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
    
    yield [
        component__none,
    ]
    
    yield (
        [
            component__text_input,
        ],
    )
    
    yield [
        component__thumbnail_media,
    ]
    
    yield [
        component__radio_group,
    ]
    
    yield [
        component__checkbox_group,
    ]
    
    yield [
        component__checkbox,
    ]
    
    # double nesting | cannot nest row into row
    yield (
        [
            [component__button],
        ],
    )
    
    # double nesting | cannot nest text display into a row
    yield (
        [
            [component__text_display],
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_components(input_value):
    """
    Tests whether ``validate_components`` works as intended.
    
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
