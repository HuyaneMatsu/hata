# Hata CLI commands

Interested in adding [cli](https://en.wikipedia.org/wiki/Command-line_interface) commands to hata or just 
got here by randomly browsing the files?

**No worries! We got you.**

> Stay still, keep reading

First you need to add your folder here with at least an `__init__.py` file in it.

##### your\_folder/\_\_init\_\_.py

In this file, you mention all commands you implemented, like:

```
Command(
    folder_name: str,
    file_name: str,
    command_name: str,
    alters: None | list<str>,
    usage: str,
    help: str,
)

Command(
    ...
)

...
```

Filled out example:

```py
__all__ = ()

from ... import Command

Command(
    'your_folder',
    'chocola',
    'chocola',
    ['choco'],
    'choco | chocola',
    'Dispalys a chocolate cake for you.',
)

Command(
    'your_folder',
    'vanilla',
    'vanilla',
    ['vani'],
    'vani | vanilla',
    'Dispalys a vanilla cake for you.',
)
```

##### your\_folder/\*

Inside of the folder you should also put your command files which you defined in your `__init__.py` file.

Each file should contain a `__main__` function accepting no parameters.

##### your\_folder/chocola.py

```py
def __main__():
    print('Here is your chocola cake')
```

##### your\_folder/vanilla.py

```py
def __main__():
    print('Here is your vanilla cake')
```