import vampytest

from ....user import User

from ..reaction_mapping_line import ReactionMappingLine


def test__ReactionMappingLine__repr():
    """
    Tests whether ``ReactionMappingLine.__repr__`` works as intended.
    """
    count = 3
    users = [
        User.precreate(202405110006),
        User.precreate(202405110007),
    ]
    
    reaction_mapping_line = ReactionMappingLine(
        count = count,
        users = users,
    )
    
    vampytest.assert_instance(repr(reaction_mapping_line), str)


def test__ReactionMappingLine__hash():
    """
    Tests whether ``ReactionMappingLine.__hash__`` works as intended.
    """
    count = 3
    users = [
        User.precreate(202405110008),
        User.precreate(202405110009),
    ]
    
    reaction_mapping_line = ReactionMappingLine(
        count = count,
        users = users,
    )
    
    vampytest.assert_instance(hash(reaction_mapping_line), int)


def test__ReactionMappingLine__eq():
    """
    Tests whether ``ReactionMappingLine.__eq__`` works as intended.
    """
    count = 3
    users = [
        User.precreate(202405110010),
        User.precreate(202405110011),
    ]
    
    keyword_parameters = {
        'count': count,
        'users': users,
    }
    
    reaction_mapping_line = ReactionMappingLine(**keyword_parameters)
    vampytest.assert_eq(reaction_mapping_line, reaction_mapping_line)
    vampytest.assert_ne(reaction_mapping_line, object())
    
    for field_name, field_value in (
        ('count', 4),
        ('users', None),
    ):
        test_reaction_mapping_line = ReactionMappingLine(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(reaction_mapping_line, test_reaction_mapping_line)


def _iter_options__len():
    user_0 = User.precreate(202405110012)
    user_1 = User.precreate(202405110013)
    
    yield {'count': 0}, 0
    yield {'count': 2}, 0
    yield {'users': []}, 0
    yield {'users': [user_0, user_1]}, 2


@vampytest._(vampytest.call_from(_iter_options__len()).returning_last())
def test__ReactionMappingLine__len(keyword_parameters):
    """
    Tests whether ``ReactionMappingLine.__len__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Parameters to test with.
    
    Returns
    -------
    output : `int`
    """
    reaction_mapping_line = ReactionMappingLine(**keyword_parameters)
    output = len(reaction_mapping_line)
    vampytest.assert_instance(output, int)
    return output


def _iter_options__iter():
    user_0 = User.precreate(202405110014)
    user_1 = User.precreate(202405110015)
    
    yield {'count': 0}, set()
    yield {'count': 2}, set()
    yield {'users': []}, set()
    yield {'users': [user_0, user_1]}, {user_0, user_1}


@vampytest._(vampytest.call_from(_iter_options__iter()).returning_last())
def test__ReactionMappingLine__iter(keyword_parameters):
    """
    Tests whether ``ReactionMappingLine.__iter__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Parameters to test with.
    
    Returns
    -------
    output : `set<ClientUserBase>`
    """
    reaction_mapping_line = ReactionMappingLine(**keyword_parameters)
    return {*reaction_mapping_line}


def _iter_options__contains():
    user_0 = User.precreate(202405110016)
    user_1 = User.precreate(202405110017)
    
    yield {'count': 0}, user_0, False
    yield {'count': 2}, user_0, False
    yield {'users': [user_0]}, user_0, True
    yield {'users': [user_1]}, user_0, False


@vampytest._(vampytest.call_from(_iter_options__contains()).returning_last())
def test__ReactionMappingLine__contains(keyword_parameters, user):
    """
    Tests whether ``ReactionMappingLine.__contains__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Parameters to test with.
    
    Returns
    -------
    output : `bool`
    """
    reaction_mapping_line = ReactionMappingLine(**keyword_parameters)
    output = user in reaction_mapping_line
    vampytest.assert_instance(output, bool)
    return output
