import vampytest

from ...radio_group_option import RadioGroupOption

from ..fields import put_options__radio_group


def _iter_options():
    option_0 = RadioGroupOption('hello')
    option_1 = RadioGroupOption('hi')

    yield (
        None,
        False,
        {
            'options': [],
        },
    )
    
    yield (
        None,
        True,
        {
            'options': [],
        },
    )
    
    yield (
        (
            option_0,
            option_1,
        ),
        False,
        {
            'options': [
                option_0.to_data(),
                option_1.to_data(),
            ],
        },
    )
    
    yield (
        (
            option_0,
            option_1,
        ),
        True,
        {
            'options': [
                option_0.to_data(defaults = True),
                option_1.to_data(defaults = True),
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_options__radio_group(input_value, defaults):
    """
    Tests whether ``put_options__radio_group`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | tuple<RadioGroupOption>``
        Input value.
    
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_options__radio_group(input_value, {}, defaults)
