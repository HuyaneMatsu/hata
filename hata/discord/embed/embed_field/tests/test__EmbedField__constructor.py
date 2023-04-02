import vampytest

from ..field import EmbedField


def _assert_fields_set(field):
    """
    Checks whether every fields of the given activity field are set.
    
    Parameters
    ----------
    field : ``EmbedField``
        The field to check.
    """
    vampytest.assert_instance(field, EmbedField)
    vampytest.assert_instance(field.inline, bool)
    vampytest.assert_instance(field.name, str, nullable = True)
    vampytest.assert_instance(field.value, str, nullable = True)


def test__EmbedField__new__0():
    """
    Tests whether ``EmbedField.__new__`` works as intended.
    
    Case: Minimal amount of parameters.
    """
    field = EmbedField()
    _assert_fields_set(field)


def test__EmbedField__new__1():
    """
    Tests whether ``EmbedField.__new__`` works as intended.
    
    Case: Maximal amount of parameters.
    """
    inline = True
    name = 'orin'
    value = 'okuu'
    
    field = EmbedField(name = name, value = value, inline = inline)
    _assert_fields_set(field)
    
    vampytest.assert_eq(field.inline, inline)
    vampytest.assert_eq(field.name, name)
    vampytest.assert_eq(field.value, value)
