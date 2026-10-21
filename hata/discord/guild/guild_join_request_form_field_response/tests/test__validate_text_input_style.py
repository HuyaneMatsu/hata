import vampytest

from ..fields import validate_text_input_style
from ..preinstanced import GuildJoinRequestFormFieldTextInputStyle


def _iter_options__passing():
    yield (
        None,
        GuildJoinRequestFormFieldTextInputStyle.short,
    )
    
    yield (
        GuildJoinRequestFormFieldTextInputStyle.paragraph,
        GuildJoinRequestFormFieldTextInputStyle.paragraph,
    )
    
    yield (
        GuildJoinRequestFormFieldTextInputStyle.paragraph.value,
        GuildJoinRequestFormFieldTextInputStyle.paragraph,
    )


def _iter_option__type_error():
    yield 12.6
    yield 'Colourful path'


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_option__type_error()).raising(TypeError))
def test__validate_text_input_style(input_value):
    output = validate_text_input_style(input_value)
    vampytest.assert_instance(output, GuildJoinRequestFormFieldTextInputStyle)
    return output
