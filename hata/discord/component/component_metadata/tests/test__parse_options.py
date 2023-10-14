import vampytest

from ...string_select_option import StringSelectOption

from ..fields import parse_options


def _iter_options():
    option_0 = StringSelectOption('hello')
    option_1 = StringSelectOption('hi')
    
    yield ({}, None)
    yield ({'options': None}, None)
    yield ({'options': []}, None)
    yield ({'options': [option_0.to_data()]}, (option_0, ))
    yield ({'options': [option_0.to_data(), option_1.to_data()]}, (option_0, option_1))


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
    output : `None | tuple<StringSelectOption>`
    """
    return parse_options(input_data)
