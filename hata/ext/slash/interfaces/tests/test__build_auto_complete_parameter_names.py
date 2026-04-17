import vampytest

from ..autocomplete import build_auto_complete_parameter_names


def _iter_options__passing():
    yield 'koishi', (), ['koishi']
    yield 'koishi', ('satori',), ['koishi', 'satori']
    yield 'koishi', ('satori', 'orin'), ['koishi', 'satori', 'orin']
    yield 'koishi', ('koishi',), ['koishi']


def _iter_options__type_error():
    yield 123.6, ()
    yield 'koishi', (12.6,)
    yield 'koishi', ('satori', 12.6)


def _iter_options__value_error():
    yield '', ()
    yield 'koishi', ('',)
    yield 'koishi', ('satori', '')


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__build_auto_complete_parameter_names(parameter_name, parameter_names):
    """
    Tests whether ``build_auto_complete_parameter_names`` works as intended.
    
    Parameters
    ----------
    parameter_name : `object`
        The parameter's name to auto complete.
    parameter_names : `tuple<object>`
        Additional parameter to autocomplete.
    
    Returns
    -------
    output : `str`
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = build_auto_complete_parameter_names(parameter_name, parameter_names)
    vampytest.assert_instance(output, list)
    return output
