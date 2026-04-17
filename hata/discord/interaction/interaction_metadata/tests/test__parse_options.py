import vampytest

from ...interaction_option import InteractionOption

from ..fields import parse_options


def _iter_options():
    option_0 = InteractionOption(name = 'requiem')
    option_1 = InteractionOption(name = 'keine')
    
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'data': None,
        },
        None,
    )
    
    yield (
        {
            'data': {},
        },
        None,
    )
    
    yield (
        {
            'data': {
                'options': None,
            },
        },
        None,
    )
    
    yield (
        {
            'data': {
                'options': [],
            },
        },
        None,
    )
    
    yield (
        {
            'data': {
                'options': [
                    option_0.to_data(),
                ],
            },
        },
        (
            option_0,
        ),
    )
    
    yield (
        {
            'data': {
                'options': [
                    option_1.to_data(),
                    option_0.to_data(),
                ],
            },
        },
        (
            option_1,
            option_0,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_options(input_data):
    """
    Tests whether ``parse_options`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | tuple<InteractionOption>``
    """
    output = parse_options(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, InteractionOption)
    
    return output
