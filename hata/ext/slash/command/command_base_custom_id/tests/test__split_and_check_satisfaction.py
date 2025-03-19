from re import compile as re_compile

import vampytest
from scarletio.utils.analyzer import Parameter

from ....converters import RegexMatcher
from ....parameter_converters.regex import ParameterConverterRegex

from ..helpers import split_and_check_satisfaction


def _create_parameter(name, *, annotation = ..., default = ...):
    """
    Creates a parameter.
    
    Parameters
    ----------
    name : `str`
        The name of teh parameter.
    
    annotation : `object`, Optional (Keyword only)
        Annotation of the parameter.
    
    default : `object`, Optional (Keyword only)
        Default value of the parameter.
    
    Returns
    -------
    parameter : ``Parameter``
    """
    parameter = object.__new__(Parameter)
    parameter.annotation = None if annotation is ... else annotation
    parameter.default = None if default is ... else default
    parameter.has_annotation = (annotation is not ...)
    parameter.has_default = (default is not ...)
    parameter.name = name
    parameter.positionality = 2
    parameter.reserved = False
    return parameter


def _iter_options__passing():
    parameter_converter_0 = ParameterConverterRegex(_create_parameter('koishi', default = 'heart'), 0)
    parameter_converter_1 = ParameterConverterRegex(_create_parameter('okuu'), 0)
    
    pattern_0 = re_compile('hey_mister')
    pattern_1 = re_compile('sister_mister')
    pattern_2 = re_compile('(hey)_mister')
    
    yield (
        'single regex',
        {
            pattern_0,
        },
        (),
        (
            None,
            (
                RegexMatcher(pattern_0),
            ),
        ),
    )
    
    yield (
        'dupe regex',
        {
            pattern_0,
            pattern_0,
        },
        (),
        (
            None,
            (
                RegexMatcher(pattern_0),
            ),
        ),
    )
    
    yield (
        'different regexes (should sort)',
        {
            pattern_0,
            pattern_1,
        },
        (),
        (
            None,
            (
                RegexMatcher(pattern_0),
                RegexMatcher(pattern_1),
            ),
        ),
    )
    
    yield (
        'single string',
        {
            'hey_sister',
        },
        (),
        (
            (
                'hey_sister',
            ),
            None,
        ),
    )
    
    yield (
        'dupe string',
        {
            'hey_sister',
            'hey_sister',
        },
        (),
        (
            (
                'hey_sister',
            ),
            None,
        ),
    )
    
    yield (
        'different string (should sort)',
        {
            'hey_sister',
            'hey_mister',
        },
        (),
        (
            (
                'hey_mister',
                'hey_sister',
            ),
            None,
        ),
    )
    
    yield (
        'string and regex',
        {
            pattern_0,
            'hey_mister',
        },
        (),
        (
            (
                'hey_mister',
            ),
            (
                RegexMatcher(pattern_0),
            ),
        ),
    )
    
    yield (
        'regex 0 + 1',
        {
            pattern_0,
        },
        (
            parameter_converter_0,
        ),
        (
            None,
            (
                RegexMatcher(pattern_0),
            ),
        ),
    )
    
    yield (
        'regex 1 + 0',
        {
            pattern_2,
        },
        (
            parameter_converter_1,
        ),
        (
            None,
            (
                RegexMatcher(pattern_2),
            ),
        ),
    )
    
    yield (
        'string 0 + 1',
        {
            'hey_mister',
        },
        (
            parameter_converter_0,
        ),
        (
            (
                'hey_mister',
            ),
            None,
        ),
    )


def _iter_options__value_error():
    parameter_converter_0 = ParameterConverterRegex(_create_parameter('koishi'), 0)
    parameter_converter_1 = ParameterConverterRegex(_create_parameter('koishi'), 0)
    
    pattern_0 = re_compile('hey_mister')
    pattern_1 = re_compile('(hey)_mister')
    
    yield (
        'regex (no group), 1 unsatisfied',
        {
            pattern_0,
        },
        (
            parameter_converter_0,
        ),
    )
    
    yield (
        'regex 1 group, 1 unsatisfied',
        {
            pattern_1,
        },
        (
            parameter_converter_0,
            parameter_converter_1,
        ),
    )
    
    yield (
        'string, 1 unsatisfied',
        {
            'hey_mister',
        },
        (
            parameter_converter_0,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options__passing()).named_first().returning_last())
@vampytest._(vampytest.call_from(_iter_options__value_error()).named_first().raising(ValueError))
def test__split_and_check_satisfaction(custom_ids, parameter_converters):
    """
    Tests whether ``split_and_check_satisfaction`` works as intended.
    
    Parameters
    ----------
    custom_ids : `set<str, re.Pattern>`
        The custom-ids to split and validate.
    
    parameter_converters : `tuple<ParameterConverterBase>`
        The parameter converters generated from a component command.
    
    Returns
    -------
    output : `(None | tuple<str>, None | tuple<RegexMatcher>)`
    
    Raises
    ------
    ValueError
    """
    output = split_and_check_satisfaction(custom_ids, parameter_converters)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    vampytest.assert_instance(output[0], tuple, nullable = True)
    vampytest.assert_instance(output[1], tuple, nullable = True)
    return output
