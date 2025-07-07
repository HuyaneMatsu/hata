import vampytest

from ....user import User

from ..reaction_mapping_line import ReactionMappingLine

from .test__ReactionMappingLine__constructor import _assert_fields_set


def test__ReactionMappingLine__copy():
    """
    Tests whether ``ReactionMappingLine.copy`` works as intended.
    """
    count = 3
    users = [
        User.precreate(202405110018),
        User.precreate(202405110019),
    ]
    
    reaction_mapping_line = ReactionMappingLine(
        count = count,
        users = users,
    )
    
    copy = reaction_mapping_line.copy()
    _assert_fields_set(copy)
    vampytest.assert_eq(reaction_mapping_line, copy)
    vampytest.assert_is_not(reaction_mapping_line, copy)


def test__ReactionMappingLine__copy_with__no_fields():
    """
    Tests whether ``ReactionMappingLine.copy`` works as intended.
    
    Case: No count
    """
    count = 3
    users = [
        User.precreate(202405110020),
        User.precreate(202405110021),
    ]
    
    reaction_mapping_line = ReactionMappingLine(
        count = count,
        users = users,
    )
    
    copy = reaction_mapping_line.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_eq(reaction_mapping_line, copy)
    vampytest.assert_is_not(reaction_mapping_line, copy)


def test__ReactionMappingLine__copy_with__all_fields():
    """
    Tests whether ``ReactionMappingLine.copy`` works as intended.
    
    Case: No count
    """
    old_count = 3
    old_users = [
        User.precreate(202405110022),
        User.precreate(202405110023),
    ]
    
    new_count = 4
    new_users = [
        User.precreate(202405110024),
        User.precreate(202405110025),
    ]
    
    reaction_mapping_line = ReactionMappingLine(
        count = old_count,
        users = old_users,
    )
    
    copy = reaction_mapping_line.copy_with(
        count = new_count,
        users = new_users,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(reaction_mapping_line, copy)
    
    vampytest.assert_eq(copy.count, new_count)
    vampytest.assert_eq(copy.users, set(new_users))


def _iter_options__merge_with():
    user_0 = User.precreate(202405110026)
    user_1 = User.precreate(202405110027)
    
    yield {'count': 1}, {'count': 1}, (1, None)
    yield {'count': 2}, {'count': 1}, (1, None)
    yield {'count': 1}, {'count': 2}, (2, None)
    yield {'count': 1, 'users': {user_0}}, {'count': 1}, (1, {user_0})
    yield {'count': 2, 'users': {user_0, user_1}}, {'count': 1}, (1, set())
    yield {'count': 1, 'users': {user_0}}, {'count': 2}, (2, set())
    yield {'count': 1, 'users': {user_0}}, {'count': 1, 'users': [user_1]}, (1, {user_1})


@vampytest._(vampytest.call_from(_iter_options__merge_with()).returning_last())
def test__ReactionMappingLine__merge_with(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ReactionMappingLine._merge_with`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create an instance.
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create an other instance.
    
    Returns
    -------
    output : ``(int, None | set<ClientUserBase>)``
    """
    reaction_mapping_line_0 = ReactionMappingLine(**keyword_parameters_0)
    reaction_mapping_line_1 = ReactionMappingLine(**keyword_parameters_1)
    reaction_mapping_line_0._merge_with(reaction_mapping_line_1)
    return reaction_mapping_line_0.count, reaction_mapping_line_0.users


def _iter_options__add_reaction():
    user_0 = User.precreate(202405110028)
    user_1 = User.precreate(202405110029)
    
    
    yield {}, user_0, (True, 1, {user_0})
    yield {'count': 1}, user_0, (True, 2, {user_0})
    yield {'count': 1, 'users': {user_0}}, user_0, (False, 1, {user_0})
    yield {'count': 1, 'users': {user_1}}, user_0, (True, 2, {user_0, user_1})


@vampytest._(vampytest.call_from(_iter_options__add_reaction()).returning_last())
def test__ReactionMappingLine__add_reaction(keyword_parameters, user):
    """
    Tests whether ``ReactionMappingLine._add_reaction`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create an instance.
    user : ``ClientUserBase``
        Voter to add.
    
    Returns
    -------
    output : `(bool, int, None | set<ClientUserBase>)`
    """
    reaction_mapping_line = ReactionMappingLine(**keyword_parameters)
    output = reaction_mapping_line._add_reaction(user)
    vampytest.assert_instance(output, bool)
    return output, reaction_mapping_line.count, reaction_mapping_line.users


def _iter_options__remove_reaction():
    user_0 = User.precreate(202405110030)
    user_1 = User.precreate(202405110031)
    
    
    yield {}, user_0, (False, 0, None)
    yield {'count': 1}, user_0, (True, 0, None)
    yield {'count': 1, 'users': {user_0}}, user_0, (True, 0, set())
    yield {'count': 1, 'users': {user_1}}, user_0, (False, 1, {user_1})
    yield {'count': 2, 'users': {user_0, user_1}}, user_0, (True, 1, {user_1})


@vampytest._(vampytest.call_from(_iter_options__remove_reaction()).returning_last())
def test__ReactionMappingLine__remove_reaction(keyword_parameters, user):
    """
    Tests whether ``ReactionMappingLine._remove_reaction`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create an instance.
    user : ``ClientUserBase``
        Voter to remove.
    
    Returns
    -------
    output : `(bool, int, None | set<ClientUserBase>)`
    """
    reaction_mapping_line = ReactionMappingLine(**keyword_parameters)
    output = reaction_mapping_line._remove_reaction(user)
    vampytest.assert_instance(output, bool)
    return output, reaction_mapping_line.count, reaction_mapping_line.users


def _iter_options__unknown():
    user_0 = User.precreate(202405110032)
    user_1 = User.precreate(202405110033)
    
    yield {}, 0
    yield {'count': 2}, 2
    yield {'count': 2, 'users': {user_0, user_1}}, 0


@vampytest._(vampytest.call_from(_iter_options__unknown()).returning_last())
def test__ReactionMappingLine__unknown(keyword_parameters):
    """
    Tests whether ``ReactionMappingLine.unknown`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create an instance.
    
    Returns
    -------
    output : `int`
    """
    reaction_mapping_line = ReactionMappingLine(**keyword_parameters)
    output = reaction_mapping_line.unknown
    vampytest.assert_instance(output, int)
    return output


def _iter_options__filter_after():
    user_0 = User.precreate(202405110034)
    user_1 = User.precreate(202405110035)
    user_2 = User.precreate(202405110036)
    user_3 = User.precreate(202405110037)
    user_4 = User.precreate(202405110038)
    
    yield {}, 2, user_1.id, []
    yield {'users': [user_0, user_1, user_2, user_3, user_4]}, 2, user_1.id, [user_2, user_3]


@vampytest._(vampytest.call_from(_iter_options__filter_after()).returning_last())
def test__ReactionMappingLine__filter_after(keyword_parameters, limit, after):
    """
    Tests whether ``ReactionMappingLine.filter_after`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create an instance.
    
    Returns
    -------
    output : `int`
    """
    reaction_mapping_line = ReactionMappingLine(**keyword_parameters)
    output = reaction_mapping_line.filter_after(limit, after)
    vampytest.assert_instance(output, list)
    return output


def _iter_options__fill_some_reactions():
    user_0 = User.precreate(202405110039)
    user_1 = User.precreate(202405110040)
    
    yield {}, [], (0, None)
    yield {'count': 1, 'users': {user_0}}, [], (1, {user_0})
    yield {}, [user_0], (1, {user_0})
    yield {'count': 1}, [user_0], (1, {user_0})
    yield {'count': 1, 'users': {user_0}}, [user_0], (1, {user_0})
    yield {'count': 1, 'users': {user_1}}, [user_0], (2, {user_0, user_1})


@vampytest._(vampytest.call_from(_iter_options__fill_some_reactions()).returning_last())
def test__ReactionMappingLine__fill_some_reactions(keyword_parameters, user):
    """
    Tests whether ``ReactionMappingLine._fill_some_reactions`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create an instance.
    users : ``list<ClientUserBase>``
        Voters to fill.
    
    Returns
    -------
    output : ``(int, None | set<ClientUserBase>)``
    """
    reaction_mapping_line = ReactionMappingLine(**keyword_parameters)
    reaction_mapping_line._fill_some_reactions(user)
    return reaction_mapping_line.count, reaction_mapping_line.users


def _iter_options__fill_all_reactions():
    user_0 = User.precreate(202405110041)
    user_1 = User.precreate(202405110042)
    
    yield {}, [], (0, None)
    yield {'count': 1, 'users': {user_0}}, [], (0, set())
    yield {}, [user_0], (1, {user_0})
    yield {'count': 1}, [user_0], (1, {user_0})
    yield {'count': 1, 'users': {user_0}}, [user_0], (1, {user_0})
    yield {'count': 1, 'users': {user_1}}, [user_0], (1, {user_0})


@vampytest._(vampytest.call_from(_iter_options__fill_all_reactions()).returning_last())
def test__ReactionMappingLine__fill_all_reactions(keyword_parameters, user):
    """
    Tests whether ``ReactionMappingLine._fill_all_reactions`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create an instance.
    users : ``list<ClientUserBase>``
        Voters to fill.
    
    Returns
    -------
    output : ``(int, None | set<ClientUserBase>)``
    """
    reaction_mapping_line = ReactionMappingLine(**keyword_parameters)
    reaction_mapping_line._fill_all_reactions(user)
    return reaction_mapping_line.count, reaction_mapping_line.users


def test__ReactionMappingLine__clear():
    """
    Tests whether ``ReactionMappingLine.clear`` works as intended.
    """
    count = 5
    
    user_0 = User.precreate(202405120000)
    user_1 = User.precreate(202405120001)
    
    reaction_mapping_line = ReactionMappingLine(
        count = count,
        users = [user_0, user_1],
    )
    
    reaction_mapping_line.clear()
    
    vampytest.assert_eq(reaction_mapping_line.count, count)
    vampytest.assert_eq(reaction_mapping_line.users, set())
