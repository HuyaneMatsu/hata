import vampytest

from ..fields import parse_type
from ..preinstanced import GuildJoinRequestFormFieldType


def _iter_options():
    yield (
        {},
        GuildJoinRequestFormFieldType.none,
    )
    
    yield (
        {
            'type': GuildJoinRequestFormFieldType.text_input_short.value,
        },
        GuildJoinRequestFormFieldType.text_input_short,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_type(input_data):
    output = parse_type(input_data)
    vampytest.assert_instance(output, GuildJoinRequestFormFieldType)
    return output
