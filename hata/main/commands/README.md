# Hata CLI commands

Interested in adding [cli](https://en.wikipedia.org/wiki/Command-line_interface) commands to hata or just 
got here by randomly browsing the files?

**No worries! We got you.**

> Stay still, keep reading

First you need to add your directory here with at least an `__init__.py` file in it.

##### your\_directory/\_\_init\_\_.py

In this file, you mention all commands you implemented, like:

```
__all__ = ()

from ... import Command

@register_command
async def vani():
    pass


@register_command(name='choco')
async def chocola():
    pass
...
```
