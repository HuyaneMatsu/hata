import vampytest

from ..expression_parser import HighlightGroup


def _assert_fields_set(highlight_group):
    """
    Asserts whether ``HighlightGroup`` has every of its attributes set.
    
    Parameters
    ----------
    highlight group : ``HighlightGroup``
        The highlight group to test.
    """
    vampytest.assert_instance(highlight_group, HighlightGroup)
    vampytest.assert_instance(highlight_group.end, int)
    vampytest.assert_instance(highlight_group.primary, bool)
    vampytest.assert_instance(highlight_group.start, int)


def test__HighlightGroup__new():
    """
    Tests whether ``HighlightGroup.__new__`` works as intended.
    """
    start = 10
    end = 12
    primary = True
    
    highlight_group = HighlightGroup(
        start,
        end,
        primary,
    )
    _assert_fields_set(highlight_group)
    
    vampytest.assert_eq(highlight_group.start, start)
    vampytest.assert_eq(highlight_group.end, end)
    vampytest.assert_eq(highlight_group.primary, primary)


def test__HighlightGroup__repr():
    """
    Tests whether ``HighlightGroup.__repr__`` works as intended.
    """
    start = 10
    end = 12
    primary = True
    
    highlight_group = HighlightGroup(
        start,
        end,
        primary,
    )
    
    output = repr(highlight_group)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_in(type(highlight_group).__name__, output)
    vampytest.assert_in(f'start = {start!r}', output)
    vampytest.assert_in(f'end = {end!r}', output)
    vampytest.assert_in(f'primary = {primary!r}', output)


def _iter_options__eq__same_type():
    yield (
        (10, 12, True),
        (10, 12, True),
        True,
    )
    
    yield (
        (9, 12, True),
        (1102, 12, True),
        False,
    )
    
    yield (
        (10, 11, True),
        (10, 12, True),
        False,
    )
    
    yield (
        (10, 12, False),
        (10, 12, True),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq__same_type()).returning_last())
def test__HighlightGroup__eq__same_type(parameters_0, parameters_1):
    """
    Tests whether ``HighlightGroup.__eq__`` works as intended.
    
    Case: same type.
    
    Parameters
    ----------
    parameters_0 : `tuple<object>`
        Parameters to create highlight group from.
    parameters_0 : `tuple<object>`
        Parameters to create highlight group from.
    
    Returns
    -------
    output : `bool`
    """
    highlight_group_0 = HighlightGroup(*parameters_0)
    highlight_group_1 = HighlightGroup(*parameters_1)
    
    output = highlight_group_0 == highlight_group_1
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__eq__different_type():
    yield None, False
    yield object(), False


@vampytest._(vampytest.call_from(_iter_options__eq__different_type()).returning_last())
def test__HighlightGroup__eq__different_type(other):
    """
    Tests whether ``HighlightGroup.__eq__`` works as intended.
    
    Case: different type.
    
    Parameters
    ----------
    other : `object`
        Other object to compare the highlight group to.
    
    Returns
    -------
    output : `bool`
    """
    start = 10
    end = 12
    primary = True
    
    highlight_group = HighlightGroup(
        start,
        end,
        primary,
    )
    
    output = highlight_group == other
    vampytest.assert_instance(output, bool)
    return output


def test__HighlightGroup__hash():
    """
    Tests whether ``HighlightGroup.__hash__`` works as intended.
    """
    start = 10
    end = 12
    primary = True
    
    highlight_group = HighlightGroup(
        start,
        end,
        primary,
    )
    
    output = hash(highlight_group)
    vampytest.assert_instance(output, int)
