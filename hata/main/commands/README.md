# Hata CLI commands

Interested in adding [cli](https://en.wikipedia.org/wiki/Command-line_interface) commands to hata or just 
got here by randomly browsing the files?

**No worries! We got you.**

> Stay still, keep reading

First you need to add your python file (like `my_file.py`), or a directory here with at least an `__init__.py` file
in it (like `my_directory/__init__.py`).

##### my\_file.py

```py3
__all__ = ()

from .. import register

@register
def vani():
    return 'Vani.'
```

##### your\_directory/\_\_init\_\_.py

When using a directory, you can define the commands in the `__init__.py` file.

```py3
__all__ = ()

from ... import register

@register
def vani():
    return 'Vani.'
```

When splitting commands logically to different files, dont forget to import them.
The entry point is always the `__init__py` file. If it is missing, the whole directory is ignored.

```py3
__all__ = ()

from .file_1 import *
from .file_2 import *
...
```

> More about command directories at [External command directories](#external-command-directories).

### Definition

Command description might be defined as a docstring, or passed as a keyword parameter.

```py3
@register
def vani():
    """Did you see choco?"""
    return 'Vani.'


@register(description='Did you see choco?')
def vani():
    return 'Vani.'
```

By default the command's name is the normalized name of the function, but with a keyword parameter it can be
overwritten too.

```py3
@register(name='vani')
def vanilla():
    return 'Vani.'
```

A command can have alternative names. These can be defined using the `alters` keyword parameter.

```py3
@register(alters=['vanilla'])
def vani():
    return 'Vani.'
```

### Parameters

You may add parameters as well, like:

```py3
@register
def vani(type_):
    """Returns you vani of the given type."""
    return f'Vani of type {type}.'
```

By default parameters are interpreted as `str`, but they can also be changed either to `bool`, `int` or `float`.

```py3
@register
def vani(type_, amount: int = 69):
    """Returns you vani of the given type."""
    return f'{amount} vani of type {type}.'
```

`bool` parameters must be keyword and they must have a default value as well.

```py3
@register
def vani(type_, amount: int = 69, *, extra_choco: bool = False):
    """Returns you vani of the given type."""
    return f'{amount} vani of type {type}{" with extra choco!" if extra_choco else ""}.'
```

`*args` and `**kwargs` parameters are also supported.

### Sub-commands

Sub-commands might be registered with the `into` keyword passed in `@register`.

```py3
@register
def main():
    return 'I am main'

@register(into=main)
def sub():
    return 'i am sub'
```

Empty command groups can be registered by passing `None` as command function.

```py3
main = register(None, name='main')

@register(into=main)
def sub():
    return 'i am sub'
```

### External command directories

When building a package you might not want to setup your files into hata. Instead magically ask hata to import them.
The `add_external_command_route` function does just this. It registers an external import route to be imported
at command lookup.

```py3
from hata.main import add_external_command_route

add_external_command_route('my_package')
```

Since you register *import routes* and not *paths* you want to use `.` to link in sub-modules.

```py3
add_external_command_route('my_package.sub_module')
```

> Note, that `hata.main` is not imported into `hata` module. So when you cannot use relative imports and want to import
> from there, specifying `.main` is necessary.
