import vampytest

from ..fields import put_type
from ..preinstanced import GuildJoinRequestFormFieldType


def _iter_options():
    yield (
        GuildJoinRequestFormFieldType.choice_single,
        False,
        {
            'type': GuildJoinRequestFormFieldType.choice_single.value,
        },
    )
    
    yield (
        GuildJoinRequestFormFieldType.choice_single,
        True,
        {
            'type': GuildJoinRequestFormFieldType.choice_single.value,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_type(input_value, defaults):
    return put_type(input_value, {}, defaults)
