"""
To set a html class to a token, do:

```py
set_highlight_html_class(token_type_identifier, html_class_name)
```

Testing
-------
To check highlights set some colors down and enjoy.

```py
TUMMY_REPR_ACCURACY = 2

class CakeEater:
    __slots__ = ('tummy_size', 'type')
    
    def __init__(self, type_, tummy_size):
        self.type = type_
        self.tummy_size = tummy_size
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.type!r}, {self.tummy_size:.{TUMMY_REPR_ACCURACY}f})'
    
    async def throw(self):
        # No one would ever expect this.
        raise StopIteration()

print(CakeEater('dream eater', 2.111))
```
"""
__all__ = ('HIGHLIGHT_TOKEN_TYPES', 'set_highlight_html_class', )

from scarletio.utils.highlight import HIGHLIGHT_TOKEN_TYPES, HighlightFormatterContext

PATCHOULI_FORMATTER_CONTEXT = HighlightFormatterContext()
PATCHOULI_FORMATTER_CONTEXT.set_highlight_html_all()


PYTHON_IDENTIFIERS = {'python', 'py', 'sage', 'python3', 'py3'}


def set_highlight_html_class(token_type_identifier, html_class):
    """
    Sets html class formatting for the given node.
    
    Parameters
    ----------
    token_type_identifier : `int`
        The node's identifier.
    html_class : `None`, `str`
        The html class to set.
    
    Raises
    ------
    TypeError
        - If `token_type_identifier` was not given as `int`.
        - If `html_class` was not given neither as `None` nor as `str`.
    ValueError
        If `token_type_identifier` was not given as any of the predefined values. Check ``TOKEN_TYPES`` for more
            details.
    """
    PATCHOULI_FORMATTER_CONTEXT.set_highlight_html_class(token_type_identifier, html_class)
