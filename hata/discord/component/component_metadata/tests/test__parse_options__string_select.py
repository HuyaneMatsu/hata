import vampytest

from ...string_select_option import StringSelectOption

from ..fields import parse_options__string_select


def _iter_options():
    option_0 = StringSelectOption('hello')
    option_1 = StringSelectOption('hi')
    
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
def test__parse_options__string_select(input_data):
    """
    Tests whether ``parse_options__string_select`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | tuple<StringSelectOption>``
    """
    output = parse_options__string_select(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, StringSelectOption)
    
    return output
