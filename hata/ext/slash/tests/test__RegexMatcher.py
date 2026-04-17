from re import I as re_ignore_case, compile as re_compile

import vampytest

from ..converters import RegexMatch, RegexMatcher

try:
    from re import Pattern
except ImportError:
    from re import _pattern_type as Pattern


def _assert_fields_set(regex_matcher):
    """
    Asserts whether every fields are set of the given regex matcher.
    
    Parameters
    ----------
    regex_matcher : ``RegexMatcher``
        The instance to check.
    """
    vampytest.assert_instance(regex_matcher, RegexMatcher)
    vampytest.assert_instance(regex_matcher.group_dict_pattern, bool)
    vampytest.assert_instance(regex_matcher.regex_pattern, Pattern)


def test__RegexMatcher__new():
    """
    Tests whether ``RegexMatch.__new__`` works as intended.
    """
    regex_pattern = re_compile('[a-z]+')
    
    regex_matcher = RegexMatcher(regex_pattern)
    _assert_fields_set(regex_matcher)
    vampytest.assert_eq(regex_matcher.regex_pattern, regex_pattern)


def _iter_options__call():
    yield (
        re_compile('[a-z]+_[a-z]+'),
        'aya',
        None,
    )
    yield (
        re_compile('[a-z]+_[a-z]+'),
        'aya_ya',
        RegexMatch(False, ()),
    )
    
    yield (
        re_compile('([a-z]+)_([a-z]+)'),
        'aya',
        None,
    )
    yield (
        re_compile('([a-z]+)_([a-z]+)'),
        'aya_ya',
        RegexMatch(False, ('aya', 'ya')),
    )
    
    yield (
        re_compile('(?P<hey>[a-z]+)_(?P<mister>[a-z]+)'),
        'aya',
        None
    )
    yield (
        re_compile('(?P<hey>[a-z]+)_(?P<mister>[a-z]+)'),
        'aya_ya',
        RegexMatch(True, {'hey': 'aya', 'mister': 'ya'}),
    )


@vampytest._(vampytest.call_from(_iter_options__call()).returning_last())
def test__RegexMatcher__call(regex_pattern, string):
    """
    Tests whether ``RegexMatch.__call__`` works as intended.
        
    Parameters
    ----------
    regex_regex_pattern : `re.Pattern`
        Regex regex pattern to create matcher for.
    
    string : `str`
        The string to match.
    
    Returns
    -------
    regex_match : `None | RegexMatch`
        The matched regex if any.
    """
    regex_matcher = RegexMatcher(regex_pattern)
    output = regex_matcher(string)
    vampytest.assert_instance(output, RegexMatch, nullable = True)
    return output


def test__RegexMatcher__repr():
    """
    Tests whether ``RegexMatch.__repr__`` works as intended.
    """
    regex_pattern = re_compile('[a-z]+')
    
    regex_matcher = RegexMatcher(regex_pattern)
    
    output = repr(regex_matcher)
    vampytest.assert_instance(output, str)


def test__RegexMatcher__hash():
    """
    Tests whether ``RegexMatch.__hash__`` works as intended.
    """
    regex_pattern = re_compile('[a-z]+')
    
    regex_matcher = RegexMatcher(regex_pattern)
    
    output = hash(regex_matcher)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    regex_pattern_0 = re_compile('[a-z]+_[a-z]+')
    regex_pattern_1 = re_compile('([a-z]+)_([a-z]+)')
    
    yield (
        {
            'regex_pattern': regex_pattern_0,
        },
        {
            'regex_pattern': regex_pattern_0,
        },
        True,
    )
    yield (
        {
            'regex_pattern': regex_pattern_0,
        },
        {
            'regex_pattern': regex_pattern_1,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__RegexMatcher__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``RegexMatcher.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    regex_matcher_0 = RegexMatcher(**keyword_parameters_0)
    regex_matcher_1 = RegexMatcher(**keyword_parameters_1)
    
    output = regex_matcher_0 == regex_matcher_1
    vampytest.assert_instance(output, bool)
    return output


def test__RegexMatcher__sort():
    """
    Tests whether ``RegexMatch`` sorting works as intended.
    """
    regex_pattern_0 = re_compile('[a-z]+')
    regex_pattern_1 = re_compile('[a-z]+', re_ignore_case)
    regex_pattern_2 = re_compile('[a-z]*')
    regex_pattern_3 = re_compile('[a-z]*', re_ignore_case)
    
    regex_matcher_0 = RegexMatcher(regex_pattern_0)
    regex_matcher_1 = RegexMatcher(regex_pattern_1)
    regex_matcher_2 = RegexMatcher(regex_pattern_2)
    regex_matcher_3 = RegexMatcher(regex_pattern_3)
    
    regex_matches = [
        regex_matcher_0,
        regex_matcher_1,
        regex_matcher_2,
        regex_matcher_3,
    ]
    
    regex_matches.sort(reverse = True)
    
    vampytest.assert_eq(
        regex_matches,
        [
            regex_matcher_1,
            regex_matcher_0,
            regex_matcher_3,
            regex_matcher_2,
        ],
    )
