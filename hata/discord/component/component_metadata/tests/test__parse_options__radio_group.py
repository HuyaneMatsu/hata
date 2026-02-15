import vampytest

from ...radio_group_option import RadioGroupOption

from ..fields import parse_options__radio_group


def _iter_options():
    option_0 = RadioGroupOption('hello')
    option_1 = RadioGroupOption('hi')
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'options': None,
        },
        None,
    )
    
    yield (
        {
            'options': [],
        },
        None,
    )
    
    yield (
        {
            'options': [
                option_0.to_data(),
                option_1.to_data(),
            ],
        },
        (
            option_0,
            option_1,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_options__radio_group(input_data):
    """
    Tests whether ``parse_options__radio_group`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | tuple<RadioGroupOption>``
    """
    output = parse_options__radio_group(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, RadioGroupOption)
    
    return output
