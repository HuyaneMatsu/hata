import vampytest

from ....application_command import ApplicationCommandTargetType

from ..fields import parse_target_type


def _iter_options():
    yield (
        {},
        ApplicationCommandTargetType.none,
    )
    
    yield (
        {
            'data': None,
        },
        ApplicationCommandTargetType.none,
    )
    
    yield (
        {
            'data': {},
        },
        ApplicationCommandTargetType.none,
    )
    
    yield (
        {
            'data': {
                'type': None,
            },
        },
        ApplicationCommandTargetType.none,
    )
    
    yield (
        {
            'data': {
                'type': ApplicationCommandTargetType.user.value,
            },
        },
        ApplicationCommandTargetType.user,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_target_type(input_data):
    """
    Tests whether ``parse_target_type`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse the target type from.
    
    Returns
    -------
    output : ``ApplicationCommandTargetType``
    """
    output = parse_target_type(input_data)
    vampytest.assert_instance(output, ApplicationCommandTargetType)
    return output
