import vampytest

from ...interaction_option import InteractionOption

from ..fields import put_options


def _iter_options():
    option_0 = InteractionOption(name = 'overkill')
    option_1 = InteractionOption(name = 'keine')

    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'data': {
                'options': [],
            },
        },
    )
    
    yield (
        (
            option_0,
        ),
        False,
        {
            'data': {
                'options': [
                    option_0.to_data(),
                ],
            },
        },
    )
    
    yield (
        (
            option_0,
        ),
        True,
        {
            'data': {
                'options': [
                    option_0.to_data(defaults = True),
                ],
            },
        },
    )
    
    yield (
        (
            option_0,
            option_1,
        ),
        False,
        {
            'data': {
                'options': [
                    option_0.to_data(),
                    option_1.to_data(),
                ],
            },
        },
    )
    
    yield (
        (
            option_0,
            option_1,
        ),
        True,
        {
            'data': {
                'options': [
                    option_0.to_data(defaults = True),
                    option_1.to_data(defaults = True),
                ],
            },
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_options(input_value, defaults):
    """
    Tests whether ``put_options`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | tuple<InteractionOption>``
        The options to serialize.
    
    defaults : `bool`
        Whether field as their default should included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_options(input_value, {}, defaults)
