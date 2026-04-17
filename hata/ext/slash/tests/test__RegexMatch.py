import vampytest

from ..converters import RegexMatch

try:
    from re import Pattern
except ImportError:
    from re import _pattern_type as Pattern


def _assert_fields_set(regex_match):
    """
    Asserts whether every fields are set of the given regex match.
    
    Parameters
    ----------
    regex_match : ``RegexMatch``
        The instance to check.
    """
    vampytest.assert_instance(regex_match, RegexMatch)
    vampytest.assert_instance(regex_match.group_dict, bool)
    vampytest.assert_instance(regex_match.groups, dict, tuple)


def test__RegexMatch__new():
    """
    Tests whether ``RegexMatch.__new__`` works as intended.
    """
    group_dict = False
    groups = ('aya', 'ya')
    
    regex_match = RegexMatch(group_dict, groups)
    _assert_fields_set(regex_match)
    
    vampytest.assert_eq(regex_match.group_dict, group_dict)
    vampytest.assert_eq(regex_match.groups, groups)


def test__RegexMatch__repr__group_tuple():
    """
    Tests whether ``RegexMatch.__repr__`` works as intended.
    
    Case: group tuple.
    """
    group_dict = False
    groups = ('aya', 'ya')
    
    regex_match = RegexMatch(group_dict, groups)
    
    output = repr(regex_match)
    vampytest.assert_instance(output, str)


def test__RegexMatch__repr__group_dict():
    """
    Tests whether ``RegexMatch.__repr__`` works as intended.
    
    Case: group dict.
    """
    group_dict = True
    groups = {'hey': 'aya', 'mister': 'ya'}
    
    regex_match = RegexMatch(group_dict, groups)
    
    output = repr(regex_match)
    vampytest.assert_instance(output, str)


def test__RegexMatch__hash__group_tuple():
    """
    Tests whether ``RegexMatch.__hash__`` works as intended.
    
    Case: group tuple.
    """
    group_dict = False
    groups = ('aya', 'ya')
    
    regex_match = RegexMatch(group_dict, groups)
    
    output = hash(regex_match)
    vampytest.assert_instance(output, int)


def test__RegexMatch__hash__group_dict():
    """
    Tests whether ``RegexMatch.__hash__`` works as intended.
    
    Case: group dict.
    """
    group_dict = True
    groups = {'hey': 'aya', 'mister': 'ya'}
    
    regex_match = RegexMatch(group_dict, groups)
    
    output = hash(regex_match)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    yield (
        {
            'group_dict': False,
            'groups': ('aya', 'ya'),
        },
        {
            'group_dict': False,
            'groups': ('aya', 'ya'),
        },
        True,
    )
    
    yield (
        {
            'group_dict': False,
            'groups': ('aya', 'ya'),
        },
        {
            'group_dict': False,
            'groups': ('aya',),
        },
        False,
    )
    
    yield (
        {
            'group_dict': True,
            'groups': {'hey': 'aya', 'mister': 'ya'},
        },
        {
            'group_dict': True,
            'groups': {'hey': 'aya', 'mister': 'ya'},
        },
        True,
    )
    
    yield (
        {
            'group_dict': True,
            'groups': {'hey': 'aya', 'mister': 'ya'},
        },
        {
            'group_dict': True,
            'groups': {'hey': 'aya'},
        },
        False,
    )

    yield (
        {
            'group_dict': False,
            'groups': ('aya', 'ya'),
        },
        {
            'group_dict': True,
            'groups': {'hey': 'aya', 'mister': 'ya'},
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__RegexMatch__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``RegexMatch.__eq__`` works as intended.
    
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
    regex_match_0 = RegexMatch(**keyword_parameters_0)
    regex_match_1 = RegexMatch(**keyword_parameters_1)
    
    output = regex_match_0 == regex_match_1
    vampytest.assert_instance(output, bool)
    return output
