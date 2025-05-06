import vampytest

from ...string_select_option import StringSelectOption

from ..fields import put_options


def _iter_options():
    option_0 = StringSelectOption('hello')
    option_1 = StringSelectOption('hi')

    yield (None, False, {'options': []})
    yield (None, True, {'options': []})
    yield (
        (option_0, option_1),
        False,
        {'options': [option_0.to_data(), option_1.to_data()]},
    )
    yield (
        (option_0, option_1),
        True,
        {'options': [option_0.to_data(defaults = True), option_1.to_data(defaults = True)]},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_options(input_value, defaults):
    """
    Tests whether ``put_options`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | tuple<StringSelectOption>``
        Input value.
    
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_options(input_value, {}, defaults)
