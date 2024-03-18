import vampytest

from ..nest_main import CONVERSION_NEST_MAIN


def _iter_options__set_validator():
    yield ('message', {'name': 'pudding'}), [('message', {'name': 'pudding'})]


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_NEST_MAIN__set_validator(input_value):
    """
    Tests whether ``CONVERSION_NEST_MAIN.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<tuple<object>>`
    """
    return [*CONVERSION_NEST_MAIN.set_validator(input_value)]


def _iter_options__serializer_putter():
    yield (
        {'content': 'hey mister'},
        False,
        ('message', {'name': 'pudding'}),
        {'name': 'pudding', 'message': {'content': 'hey mister'}},
    )
    yield (
        {'content': 'hey mister'},
        True,
        ('message', {'name': 'pudding'}),
        {'name': 'pudding', 'message': {'content': 'hey mister'}},
    )
    yield (
        {},
        False,
        ('message', {'name': 'pudding'}),
        {'name': 'pudding'},
    )
    yield (
        {},
        True,
        ('message', {'name': 'pudding'}),
        {'name': 'pudding', 'message': {}},
    )


@vampytest._(vampytest.call_from(_iter_options__serializer_putter()).returning_last())
def test__CONVERSION_NEST_MAIN__set_validator(main_data, required, value):
    """
    Tests whether ``CONVERSION_NEST_MAIN.serializer_putter`` works as intended.
    
    Parameters
    ----------
    main_data : `dict<str, object>`
        Already existing data.
    required : `bool`
        Whether should include defaults.
    value : `tuple<str, dict<str, object>>`
        Value to serialize.
    
    Returns
    -------
    output : `list<tuple<object>>`
    """
    main_data.copy()
    value = (value[0], value[1].copy())
    
    return CONVERSION_NEST_MAIN.serializer_putter(main_data, required, value)
