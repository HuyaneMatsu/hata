import vampytest

from ..audit_log_change import AuditLogChange
from ..flags import FLAG_HAS_AFTER, FLAG_HAS_BEFORE


def _assert_fields_set(change):
    """
    Asserts whether every fields are set of the given audit log change.
    
    Parameters
    ----------
    change : ``AuditLogChange``
    """
    vampytest.assert_instance(change, AuditLogChange)
    vampytest.assert_instance(change.after, object)
    vampytest.assert_instance(change.attribute_name, str)
    vampytest.assert_instance(change.before, object)
    vampytest.assert_instance(change.flags, int)


def test__AuditLogChange__new__minimal_fields():
    """
    Tests whether ``AuditLogChange.__new__`` works as intended.
    
    Case: minimal fields given.
    """
    attribute_name = 'koishi'
    
    change = AuditLogChange(attribute_name)
    _assert_fields_set(change)
    
    vampytest.assert_eq(change.attribute_name, attribute_name)
    vampytest.assert_eq(change.flags, 0)


def test__AuditLogChange__new__all_fields():
    """
    Tests whether ``AuditLogChange.__new__`` works as intended.
    
    Case: all fields given.
    """
    attribute_name = 'koishi'
    before = 1
    after = 2
    
    change = AuditLogChange(attribute_name, before = before, after = after)
    _assert_fields_set(change)
    
    vampytest.assert_eq(change.attribute_name, attribute_name)
    vampytest.assert_eq(change.flags, FLAG_HAS_AFTER | FLAG_HAS_BEFORE)
    vampytest.assert_eq(change.after, after)
    vampytest.assert_eq(change.before, before)
    

def test__AuditLogChange__create_clean():
    """
    Tests whether ``AuditLogChange.create_clean`` works as intended.
    """
    attribute_name = 'koishi'
    
    change = AuditLogChange.create_clean(attribute_name)
    _assert_fields_set(change)
    
    vampytest.assert_eq(change.attribute_name, attribute_name)
    vampytest.assert_eq(change.flags, 0)
    vampytest.assert_is(change.after, None)
    vampytest.assert_is(change.before, None)


def test__AuditLogChange__from_fields():
    """
    Tests whether ``AuditLogChange.from_fields`` works as intended.
    """
    attribute_name = 'koishi'
    flags = FLAG_HAS_BEFORE
    before = 1
    after = 2
    
    change = AuditLogChange.from_fields(attribute_name, flags, before, after)
    _assert_fields_set(change)
    
    vampytest.assert_eq(change.attribute_name, attribute_name)
    vampytest.assert_eq(change.flags, flags)
    vampytest.assert_eq(change.after, after)
    vampytest.assert_eq(change.before, before)


def test__AuditLogChange__repr():
    """
    Tests whether ``AuditLogChange.__repr__`` works as intended.
    """
    attribute_name = 'koishi'
    before = 1
    after = 2
    
    change = AuditLogChange(attribute_name, before = before, after = after)
    
    vampytest.assert_instance(repr(change), str)


def test__AuditLogChange__hash():
    """
    Tests whether ``AuditLogChange.__hash__`` works as intended.
    """
    attribute_name = 'koishi'
    before = 1
    after = 2
    
    change = AuditLogChange(attribute_name, before = before, after = after)
    
    vampytest.assert_instance(hash(change), int)


def test__AuditLogChange__eq():
    """
    Tests whether ``AuditLogChange.__hash__`` works as intended.
    """
    attribute_name = 'koishi'
    before = 1
    after = 2
    
    keyword_parameters = {
        'attribute_name': attribute_name,
        'before': before,
        'after': after,
    }
    
    change = AuditLogChange(**keyword_parameters)
    vampytest.assert_eq(change, change)
    vampytest.assert_ne(change, object())
    
    for field_name, field_value in (
        ('attribute_name', 'komeiji'),
        ('before', 3),
        ('after', 4),
    ):
        test_change = AuditLogChange(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(change, test_change)
    

def _iter_options():
    attribute_name = 'koishi'
    yield AuditLogChange(attribute_name), AuditLogChange.has_before, False
    yield AuditLogChange(attribute_name, before = False), AuditLogChange.has_before, True
    yield AuditLogChange(attribute_name), AuditLogChange.has_after, False
    yield AuditLogChange(attribute_name, after = False), AuditLogChange.has_after, True


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__AuditLogChange__checks(change, check):
    """
    Tests whether an ``AuditLogChange``'s checks work as intended.
    
    Parameters
    ----------
    change : ``AuditLogChange``
        Change to test with.
    check : `FunctionType | MethodType`
        Check to run.
    
    Returns
    -------
    output : `bool`
    """
    output = check(change)
    vampytest.assert_instance(output, bool)
    return output
