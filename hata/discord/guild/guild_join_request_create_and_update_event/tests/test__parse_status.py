import vampytest

from ...guild_join_request import GuildJoinRequestStatus

from ..fields import parse_status


def _iter_options():
    yield (
        {},
        GuildJoinRequestStatus.started,
    )
    
    yield (
        {
            'status': None,
        },
        GuildJoinRequestStatus.started,
    )
    
    yield (
        {
            'status': GuildJoinRequestStatus.pending.value,
        },
        GuildJoinRequestStatus.pending,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_status(input_data):
    output = parse_status(input_data)
    vampytest.assert_instance(output, GuildJoinRequestStatus)
    return output
